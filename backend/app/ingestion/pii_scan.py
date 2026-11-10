"""Content-level PII scan for ingested sources (Phase 14A — Presidio + BERT).

Engine selection
----------------
The active engine is chosen at startup from the ``PII_ENGINE`` environment
variable (default ``"presidio"``):

  ``presidio``  Use Presidio + BERT / spaCy (Phase 14A).  Falls back to the
                Phase 11K regex engine if ``presidio_analyzer`` is not
                installed.
  ``regex``     Force the Phase 11K regex engine regardless of whether
                Presidio is available.  Useful for lightweight deployments or
                test environments.

Security contract (preserved and unchanged from Phase 12C)
----------------------------------------------------------
  * The scan is best-effort and NEVER rewrites the stored source.  The
    original file and extracted text are left untouched.
  * Only non-secret category counts are stored/emitted.  Raw PII values are
    never persisted here and never attached to audit events.
  * Missing/unreadable text yields a clean "no findings" summary so the
    ingestion path is never blocked by the scan.

Category ordering
-----------------
The ``counts`` dict returned by :func:`scan_source_pii` uses a stable
ordering so downstream callers and tests can rely on key order.  Categories
detected by the Presidio engine extend the Phase 11K set with contextual
entities (person, location, organization, etc.).
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Stable metadata / event keys (unchanged from Phase 12C).
META_KEY = "pii_scan"
EVENT_TYPE = "pii_detected"
_DETECTED_KEY = "detected"
_COUNTS_KEY = "counts"

# Deterministic category ordering — Phase 11K categories first so existing
# consumers are unaffected; Presidio-only categories appended in alphabetical
# order.
_CATEGORY_ORDER = (
    # Phase 11K (regex engine)
    "email",
    "phone",
    "ipv4",
    "credit_card",
    # Phase 14A (Presidio / BERT)
    "person",
    "location",
    "organization",
    "aadhaar",
    "pan",
    "passport",
    "voter_id",
    "date_time",
    "nrp",
    "url",
)

# ---------------------------------------------------------------------------
# Engine selection
# ---------------------------------------------------------------------------


def _selected_engine() -> str:
    env_val = os.environ.get("PII_ENGINE")
    if env_val is not None:
        return env_val.strip().lower()
    try:
        from app.core.config import settings

        return str(settings.PII_ENGINE).strip().lower()
    except Exception:
        return "presidio"


def _use_presidio() -> bool:
    """Return True if the Presidio engine should be used."""
    if _selected_engine() == "regex":
        return False
    # Lazy import — only pay the import cost if Presidio is requested.
    try:
        from app.core.presidio_engine import presidio_available
        return presidio_available()
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Public scan API
# ---------------------------------------------------------------------------

def scan_source_pii(text: str | None) -> dict[str, Any]:
    """Return a bounded PII-scan summary for normalized source text.

    Returns a dict of the form ``{"detected": bool, "counts": {category: n},
    "engine": str}`` where:

    * ``counts`` contains only categories with at least one finding, in the
      stable order defined by ``_CATEGORY_ORDER``.
    * ``engine`` records which back-end was used (``"presidio"`` or
      ``"regex"``) so the audit trail is transparent.
    * Raw PII values are never included.
    * Empty / None text yields ``detected=False`` with an empty counts dict.

    Parameters
    ----------
    text : str | None
        Normalized document text extracted from an ingested source.
    """
    if not text:
        return {_DETECTED_KEY: False, _COUNTS_KEY: {}, "engine": "none"}

    if _use_presidio():
        return _scan_presidio(text)
    return _scan_regex(text)


# ---------------------------------------------------------------------------
# Presidio engine path
# ---------------------------------------------------------------------------

def _scan_presidio(text: str) -> dict[str, Any]:
    """Run the Presidio + BERT scan and return the standard summary dict."""
    try:
        from app.core.presidio_engine import detect_pii_presidio

        findings = detect_pii_presidio(text)
    except Exception as exc:
        logger.warning(
            "Presidio PII scan failed; falling back to regex engine. Error: %s", exc
        )
        return _scan_regex(text)

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1

    ordered = {k: counts[k] for k in _CATEGORY_ORDER if counts.get(k)}
    # Preserve any categories not in the predefined order (future-proof).
    for k, v in counts.items():
        if k not in ordered:
            ordered[k] = v

    return {_DETECTED_KEY: bool(ordered), _COUNTS_KEY: ordered, "engine": "presidio"}


# ---------------------------------------------------------------------------
# Phase 11K regex fallback path
# ---------------------------------------------------------------------------

def _scan_regex(text: str) -> dict[str, Any]:
    """Run the Phase 11K deterministic regex scan."""
    from app.core.pii import detect_pii

    counts: dict[str, int] = {}
    findings = detect_pii(text)
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1

    ordered = {k: counts[k] for k in _CATEGORY_ORDER if counts.get(k)}
    return {_DETECTED_KEY: bool(ordered), _COUNTS_KEY: ordered, "engine": "regex"}
