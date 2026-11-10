"""
KaryaSetu Backend — Presidio + BERT PII Engine (Phase 14A)

Wraps Microsoft Presidio with the ``dslim/bert-base-NER`` Hugging Face
Transformer model as the NLP back-end.  Presidio orchestrates:

  * BERT NER  — contextual detection of PERSON, LOCATION, ORGANIZATION.
  * Built-in pattern recognizers — EMAIL_ADDRESS, PHONE_NUMBER, IP_ADDRESS,
    CREDIT_CARD (with Luhn).
  * Custom Indian-ID recognizers — Aadhaar (regex + Verhoeff checksum),
    PAN Card, Indian Passport, Voter ID (EPIC).

Architecture
------------
The existing ``app.core.pii`` module (Phase 11K) remains UNCHANGED.  It is
still used for ultra-low-latency log/surface scrubbing (regex only, no model
loading).  This module is the **document-content** engine used by the
ingestion pipeline (``app.ingestion.pii_scan``).

Design contracts (unchanged from Phase 11K)
-------------------------------------------
  * Detection NEVER rewrites stored source files.  Redaction is applied only
    to metadata, audit events, and log surfaces.
  * Raw PII values are NEVER persisted or attached to audit events.
  * A missing / unavailable NLP model degrades gracefully: the engine falls
    back from BERT (Transformers) -> spaCy -> Presidio pattern recognizers ->
    Phase 11K regex engine.
  * First call is intentionally lazy — the BERT model is loaded on demand so
    import cost is zero at startup.

Configuration (env vars or ``.env`` via ``app.core.config.settings``)
-----------------------------------------------------------------------
``PII_ENGINE``           : ``"presidio"`` (default) | ``"regex"``
``PII_NLP_BACKEND``      : ``"transformers"`` (default) | ``"spacy"``
``PII_BERT_MODEL``       : HuggingFace model ID (default ``"dslim/bert-base-NER"``)
``PII_SCORE_THRESHOLD``  : Float in [0, 1] (default ``0.35``)
``PII_CHUNK_SIZE``       : Whitespace-token chunk size (default ``400``)
``PII_CHUNK_OVERLAP``    : Overlap tokens between chunks (default ``50``)
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config resolution (env vars override Settings / .env)
# ---------------------------------------------------------------------------


def _cfg_str(name: str, default: str) -> str:
    env_val = os.environ.get(name)
    if env_val is not None:
        return env_val
    try:
        from app.core.config import settings

        return str(getattr(settings, name, default))
    except Exception:
        return default


def _cfg_float(name: str, default: float) -> float:
    env_val = os.environ.get(name)
    if env_val is not None:
        return float(env_val)
    try:
        from app.core.config import settings

        return float(getattr(settings, name, default))
    except Exception:
        return default


def _cfg_int(name: str, default: int) -> int:
    env_val = os.environ.get(name)
    if env_val is not None:
        return int(env_val)
    try:
        from app.core.config import settings

        return int(getattr(settings, name, default))
    except Exception:
        return default


# Keep module-level defaults exported for backward compatibility / tests.
_SCORE_THRESHOLD = _cfg_float("PII_SCORE_THRESHOLD", 0.35)
_CHUNK_SIZE = _cfg_int("PII_CHUNK_SIZE", 400)
_CHUNK_OVERLAP = _cfg_int("PII_CHUNK_OVERLAP", 50)

# Presidio entity types to request from the analyzer.
# Deliberately excludes noisy generic types (DATE_TIME, URL, NRP) so everyday
# words like "quarterly" or domains inside emails do not trigger false positives.
_ENTITIES = [
    "PERSON",
    "LOCATION",
    "ORGANIZATION",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "IP_ADDRESS",
    "CREDIT_CARD",
    # Custom Indian identifiers registered below.
    "IN_AADHAAR",
    "IN_PAN",
    "IN_PASSPORT",
    "IN_VOTER_ID",
]

# Map Presidio entity types -> canonical category labels used by the existing
# ``PIIFinding`` dataclass and ``pii_scan`` metadata keys.
_ENTITY_TO_CATEGORY: dict[str, str] = {
    "PERSON": "person",
    "LOCATION": "location",
    "ORGANIZATION": "organization",
    "EMAIL_ADDRESS": "email",
    "PHONE_NUMBER": "phone",
    "IP_ADDRESS": "ipv4",
    "CREDIT_CARD": "credit_card",
    "DATE_TIME": "date_time",
    "NRP": "nrp",
    "URL": "url",
    "IN_AADHAAR": "aadhaar",
    "IN_PAN": "pan",
    "IN_PASSPORT": "passport",
    "IN_VOTER_ID": "voter_id",
}

# Map dslim/bert-base-NER BIO-aggregated output labels to Presidio entity names.
_BERT_ENTITY_MAPPING: dict[str, str] = {
    "PER": "PERSON",
    "PERSON": "PERSON",
    "ORG": "ORGANIZATION",
    "ORGANIZATION": "ORGANIZATION",
    "LOC": "LOCATION",
    "LOCATION": "LOCATION",
    "MISC": "MISC",
}

# ---------------------------------------------------------------------------
# Verhoeff algorithm — Aadhaar checksum
# ---------------------------------------------------------------------------


class _Verhoeff:
    """Deterministic Verhoeff checksum used to validate 12-digit Aadhaar numbers."""

    _D = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    ]
    _P = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
    ]

    @classmethod
    def validate(cls, num_str: str) -> bool:
        digits = [int(c) for c in num_str if c.isdigit()]
        if len(digits) != 12:
            return False
        c = 0
        for i, digit in enumerate(reversed(digits)):
            c = cls._D[c][cls._P[i % 8][digit]]
        return c == 0


# ---------------------------------------------------------------------------
# Custom Indian-ID Pattern Recognizers
# ---------------------------------------------------------------------------


def _build_indian_recognizers() -> list[Any]:
    """Build Presidio PatternRecognizer objects for Indian national IDs.

    Returns an empty list if presidio_analyzer is not installed (graceful
    degradation path).
    """
    try:
        from presidio_analyzer import Pattern, PatternRecognizer
    except ImportError:
        return []

    class AadhaarRecognizer(PatternRecognizer):
        """12-digit Aadhaar with Verhoeff checksum validation."""

        PATTERNS = [
            Pattern(
                name="aadhaar",
                regex=r"\b[2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}\b",
                score=0.5,
            )
        ]

        def __init__(self) -> None:
            super().__init__(
                supported_entity="IN_AADHAAR",
                patterns=self.PATTERNS,
                name="AadhaarRecognizer",
                supported_language="en",
            )

        def validate_result(self, pattern_text: str) -> bool | None:
            return _Verhoeff.validate(pattern_text)

    class PanRecognizer(PatternRecognizer):
        """10-character Indian PAN card (format validated by regex structure)."""

        PATTERNS = [
            Pattern(
                name="pan",
                regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
                score=0.85,
            )
        ]

        def __init__(self) -> None:
            super().__init__(
                supported_entity="IN_PAN",
                patterns=self.PATTERNS,
                name="PanRecognizer",
                supported_language="en",
            )

    class PassportRecognizer(PatternRecognizer):
        """Indian passport number: 1 uppercase letter + 1 non-zero digit + 6 digits (8 chars)."""

        PATTERNS = [
            Pattern(
                name="in_passport",
                regex=r"\b[A-Z][1-9]\d{6}\b",
                score=0.6,
            )
        ]

        def __init__(self) -> None:
            super().__init__(
                supported_entity="IN_PASSPORT",
                patterns=self.PATTERNS,
                name="PassportRecognizer",
                supported_language="en",
            )

    class VoterIdRecognizer(PatternRecognizer):
        """Indian Voter ID / EPIC: 3 uppercase letters + 7 digits."""

        PATTERNS = [
            Pattern(
                name="epic",
                regex=r"\b[A-Z]{3}[0-9]{7}\b",
                score=0.6,
            )
        ]

        def __init__(self) -> None:
            super().__init__(
                supported_entity="IN_VOTER_ID",
                patterns=self.PATTERNS,
                name="VoterIdRecognizer",
                supported_language="en",
            )

    return [
        AadhaarRecognizer(),
        PanRecognizer(),
        PassportRecognizer(),
        VoterIdRecognizer(),
    ]


# ---------------------------------------------------------------------------
# Engine construction (lazy, singleton)
# ---------------------------------------------------------------------------


def _build_transformers_nlp_engine(bert_model: str) -> Any | None:
    """Return a loaded Transformers (BERT) NLP engine or None on failure."""
    try:
        from presidio_analyzer.nlp_engine import (
            NerModelConfiguration,
            TransformersNlpEngine,
        )

        ner_config = NerModelConfiguration(
            model_to_presidio_entity_mapping=_BERT_ENTITY_MAPPING,
            labels_to_ignore=["O"],
            aggregation_strategy="simple",
        )
        engine = TransformersNlpEngine(
            models=[
                {
                    "lang_code": "en",
                    "model_name": {
                        "spacy": "en_core_web_sm",
                        "transformers": bert_model,
                    },
                }
            ],
            ner_model_configuration=ner_config,
        )
        # Load eagerly inside try/except so missing weights or models trigger
        # the fallback chain immediately rather than failing during analyze().
        engine.load()
        logger.info(
            "Presidio NLP engine initialised (backend=transformers, model=%s)",
            bert_model,
        )
        return engine
    except Exception as exc:
        logger.warning(
            "BERT/Transformers NLP engine failed to load; falling back to "
            "spaCy NLP engine for Presidio. Error: %s",
            exc,
        )
        return None


def _build_spacy_nlp_engine() -> Any | None:
    """Return a loaded spaCy-backed NLP engine or None if unavailable."""
    try:
        from presidio_analyzer.nlp_engine import SpacyNlpEngine

        engine = SpacyNlpEngine(
            models=[{"lang_code": "en", "model_name": "en_core_web_sm"}]
        )
        engine.load()
        logger.info("Presidio NLP engine initialised (backend=spacy)")
        return engine
    except Exception as exc:
        logger.warning("spaCy NLP engine unavailable: %s", exc)
        return None


@lru_cache(maxsize=1)
def _build_analyzer() -> Any | None:
    """Build and cache the Presidio AnalyzerEngine (called once per process).

    Returns ``None`` if presidio_analyzer is not installed — the caller must
    handle this gracefully.
    """
    try:
        from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
    except ImportError:
        logger.warning(
            "presidio_analyzer not installed; PII engine will fall back to "
            "Phase 11K regex engine. Install with: pip install presidio-analyzer[transformers]"
        )
        return None

    registry = RecognizerRegistry()
    registry.load_predefined_recognizers(languages=["en"])

    for recognizer in _build_indian_recognizers():
        registry.add_recognizer(recognizer)

    nlp_backend = _cfg_str("PII_NLP_BACKEND", "transformers").lower()
    bert_model = _cfg_str("PII_BERT_MODEL", "dslim/bert-base-NER")

    nlp_engine = None
    if nlp_backend == "transformers":
        nlp_engine = _build_transformers_nlp_engine(bert_model)
    if nlp_engine is None:
        nlp_engine = _build_spacy_nlp_engine()

    if nlp_engine is None:
        logger.warning(
            "No NLP engine available; Presidio will use pattern recognizers only "
            "(no PERSON / LOCATION / ORGANIZATION detection)."
        )
        return AnalyzerEngine(registry=registry, supported_languages=["en"])

    return AnalyzerEngine(
        nlp_engine=nlp_engine,
        registry=registry,
        supported_languages=["en"],
    )


# ---------------------------------------------------------------------------
# Sliding-window chunker
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"\S+")


def _word_chunks(
    text: str,
    size: int | None = None,
    overlap: int | None = None,
) -> list[tuple[str, int]]:
    """Split *text* into overlapping slices preserving exact character offsets.

    BERT has a 512-token hard limit.  This chunker slices the original *text*
    between whitespace-delimited token boundaries rather than re-joining tokens,
    guaranteeing ``char_offset + local_index == global_index`` even across
    newlines, tabs, and irregular whitespace.

    Returns a list of ``(chunk_text, char_offset)`` pairs.
    """
    if not text:
        return []

    chunk_size = size if size is not None else _cfg_int("PII_CHUNK_SIZE", 400)
    chunk_overlap = overlap if overlap is not None else _cfg_int("PII_CHUNK_OVERLAP", 50)
    chunk_size = max(1, chunk_size)
    chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))

    tokens = [(m.start(), m.end()) for m in _TOKEN_RE.finditer(text)]
    if not tokens:
        return []

    chunks: list[tuple[str, int]] = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        char_start = tokens[start][0]
        char_end = tokens[end - 1][1]
        chunks.append((text[char_start:char_end], char_start))
        if end == len(tokens):
            break
        start += step

    return chunks


# ---------------------------------------------------------------------------
# Public dataclass (mirrors app.core.pii.PIIFinding for compatibility)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PresidioFinding:
    """One PII finding from the Presidio engine.

    Attributes
    ----------
    category : str
        Canonical lower-case category label (e.g. ``"person"``, ``"email"``).
    entity_type : str
        Raw Presidio entity type (e.g. ``"PERSON"``, ``"EMAIL_ADDRESS"``).
    score : float
        Presidio confidence score in [0, 1].
    redacted_snippet : str
        Safe log-friendly marker — never the raw PII value.
    """

    category: str
    entity_type: str
    score: float
    redacted_snippet: str


# ---------------------------------------------------------------------------
# Chunk analysis helper (global offset mapping + overlap deduplication)
# ---------------------------------------------------------------------------


def _analyze_chunked(analyzer: Any, text: str) -> list[Any]:
    """Run *analyzer* across overlapping chunks and deduplicate global spans."""
    from presidio_analyzer import RecognizerResult

    threshold = _cfg_float("PII_SCORE_THRESHOLD", 0.35)
    best_by_span: dict[tuple[str, int, int], Any] = {}

    for chunk_text, char_offset in _word_chunks(text):
        try:
            results = analyzer.analyze(
                text=chunk_text,
                entities=_ENTITIES,
                language="en",
                score_threshold=threshold,
            )
        except Exception as exc:
            logger.warning("Presidio analyze error on chunk: %s", exc)
            continue

        for result in results:
            global_start = char_offset + result.start
            global_end = char_offset + result.end
            key = (result.entity_type, global_start, global_end)
            existing = best_by_span.get(key)
            if existing is None or result.score > existing.score:
                best_by_span[key] = RecognizerResult(
                    entity_type=result.entity_type,
                    start=global_start,
                    end=global_end,
                    score=result.score,
                )

    return sorted(best_by_span.values(), key=lambda r: (r.start, -r.score))


# ---------------------------------------------------------------------------
# Main public API
# ---------------------------------------------------------------------------


def detect_pii_presidio(text: str) -> list[PresidioFinding]:
    """Detect PII in *text* using the Presidio + BERT engine.

    The function is intentionally best-effort:
    * Returns ``[]`` for empty/None input.
    * Deduplicates entities falling inside chunk overlap windows while
      preserving separate occurrences at different positions in the document.
    * Falls back to ``[]`` if the Presidio engine is unavailable.
    """
    if not text:
        return []

    analyzer = _build_analyzer()
    if analyzer is None:
        return []

    findings: list[PresidioFinding] = []
    for result in _analyze_chunked(analyzer, text):
        entity_type: str = result.entity_type
        category = _ENTITY_TO_CATEGORY.get(entity_type, entity_type.lower())
        findings.append(
            PresidioFinding(
                category=category,
                entity_type=entity_type,
                score=result.score,
                redacted_snippet=f"[PII:{entity_type}]",
            )
        )

    return findings


def redact_pii_presidio(text: str) -> str:
    """Return *text* with detected PII values replaced by category markers.

    Analyzes across overlapping chunks, maps spans back to exact global offsets,
    and invokes ``AnonymizerEngine`` once on the original *text* so original
    whitespace/newlines are preserved without duplicating overlap regions.
    """
    if not text:
        return text

    try:
        from presidio_anonymizer import AnonymizerEngine
        from presidio_anonymizer.entities import OperatorConfig
    except ImportError:
        logger.warning(
            "presidio_anonymizer not installed; redact_pii_presidio returning "
            "original text. Install with: pip install presidio-anonymizer"
        )
        return text

    analyzer = _build_analyzer()
    if analyzer is None:
        return text

    try:
        global_results = _analyze_chunked(analyzer, text)
        if not global_results:
            return text
        operators = {
            entity: OperatorConfig("replace", {"new_value": f"[PII:{entity}]"})
            for entity in _ENTITIES
        }
        anonymized = AnonymizerEngine().anonymize(
            text=text,
            analyzer_results=global_results,
            operators=operators,
        )
        return anonymized.text
    except Exception as exc:
        logger.warning("Presidio anonymize error: %s", exc)
        return text


def presidio_available() -> bool:
    """Return True if the Presidio engine can be loaded (lazy, cached)."""
    return _build_analyzer() is not None


__all__ = [
    "PresidioFinding",
    "detect_pii_presidio",
    "redact_pii_presidio",
    "presidio_available",
    "_Verhoeff",
    "_word_chunks",
]
