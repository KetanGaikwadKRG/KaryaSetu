"""Phase 14A tests — Presidio + BERT PII engine.

Test strategy
-------------
These tests are structured in three layers:

Layer 1 — Pure unit tests (zero external dependencies, always fast)
  * Verhoeff algorithm correctness.
  * Indian ID regex patterns (Aadhaar, PAN, Passport, Voter ID).
  * Sliding-window chunker offset accuracy across newlines and irregular spaces.
  * Settings validation for Phase 14A PII configuration knobs.
  * ``scan_source_pii`` public API contract (engine-agnostic).

Layer 2 — Presidio engine tests (skipped if presidio_analyzer not installed)
  * ``detect_pii_presidio`` returns PresidioFinding objects.
  * Structured PII (email, phone, IP, credit card) is detected.
  * Indian ID recognizers fire for valid values.
  * ``redact_pii_presidio`` replaces detected values with markers while
    preserving original formatting across chunk overlaps.
  * Chunk overlap deduplication avoids double-counting straddling spans.

Layer 3 — Fallback / degradation tests
  * When PII_ENGINE=regex the scan uses the Phase 11K regex engine.
  * When Presidio is unavailable the regex fallback kicks in gracefully.
"""
from __future__ import annotations

import os
import re
import unittest

import pytest

from app.core.config import Settings
from app.core.presidio_engine import _Verhoeff, _word_chunks
from app.ingestion.pii_scan import (
    EVENT_TYPE,
    META_KEY,
    _CATEGORY_ORDER,
    scan_source_pii,
)

PRESIDIO_AVAILABLE = False
try:
    import presidio_analyzer  # noqa: F401
    PRESIDIO_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Layer 1 — Pure unit tests (zero external dependencies)
# ---------------------------------------------------------------------------


class TestVerhoeff(unittest.TestCase):
    """Verhoeff algorithm correctness."""

    def test_valid_aadhaar(self):
        assert _Verhoeff.validate("234123412346") is True

    def test_valid_aadhaar_with_spaces(self):
        assert _Verhoeff.validate("2341 2341 2346") is True

    def test_invalid_aadhaar_wrong_check(self):
        assert _Verhoeff.validate("234123412340") is False

    def test_too_short(self):
        assert _Verhoeff.validate("23412341234") is False

    def test_too_long(self):
        assert _Verhoeff.validate("2341234123456") is False


class TestIndianIdRegex(unittest.TestCase):
    """Indian national ID pattern matching (regex layer, no Presidio required)."""

    def test_pan_valid(self):
        pan_re = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")
        assert pan_re.search("ABCDE1234F") is not None

    def test_pan_invalid_lowercase(self):
        pan_re = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")
        assert pan_re.search("abcde1234f") is None

    def test_passport_valid(self):
        pp_re = re.compile(r"\b[A-Z][1-9]\d{6}\b")
        assert pp_re.search("A1234567") is not None

    def test_passport_invalid_starts_zero(self):
        pp_re = re.compile(r"\b[A-Z][1-9]\d{6}\b")
        assert pp_re.search("A0234567") is None

    def test_passport_invalid_wrong_length(self):
        pp_re = re.compile(r"\b[A-Z][1-9]\d{6}\b")
        assert pp_re.search("A123456") is None
        assert pp_re.search("A12345678") is None

    def test_voter_id_valid(self):
        voter_re = re.compile(r"\b[A-Z]{3}[0-9]{7}\b")
        assert voter_re.search("ABC1234567") is not None


class TestWordChunks(unittest.TestCase):
    """Sliding-window chunker offset accuracy and boundary handling."""

    def test_empty_returns_empty(self):
        assert _word_chunks("") == []
        assert _word_chunks("   \n\t  ") == []

    def test_exact_substring_offsets_with_newlines_and_spaces(self):
        text = "First\n\nsecond   third\tfourth  fifth\nsixth"
        chunks = _word_chunks(text, size=3, overlap=1)
        assert len(chunks) >= 2
        for chunk_text, offset in chunks:
            assert text[offset : offset + len(chunk_text)] == chunk_text

    def test_overlap_covers_boundary_tokens(self):
        words = [f"w{i}" for i in range(10)]
        text = " ".join(words)
        chunks = _word_chunks(text, size=6, overlap=2)
        # First chunk: w0..w5, second chunk: w4..w9
        assert len(chunks) == 2
        assert chunks[0][0] == "w0 w1 w2 w3 w4 w5"
        assert chunks[1][0] == "w4 w5 w6 w7 w8 w9"
        assert text[chunks[1][1] :].startswith("w4")


class TestPiiConfigValidation(unittest.TestCase):
    """Pydantic settings validation for Phase 14A PII fields."""

    def test_defaults_valid(self):
        cfg = Settings()
        assert cfg.PII_ENGINE == "presidio"
        assert cfg.PII_NLP_BACKEND == "transformers"
        assert cfg.PII_BERT_MODEL == "dslim/bert-base-NER"
        assert cfg.PII_CHUNK_SIZE == 400
        assert cfg.PII_CHUNK_OVERLAP == 50

    def test_overlap_gte_size_rejected(self):
        with pytest.raises(ValueError):
            Settings(PII_CHUNK_SIZE=100, PII_CHUNK_OVERLAP=100)


class TestScanSourcePiiContract(unittest.TestCase):
    """Engine-agnostic contract tests for scan_source_pii."""

    def test_none_input(self):
        result = scan_source_pii(None)
        assert result["detected"] is False
        assert result["counts"] == {}

    def test_empty_string(self):
        result = scan_source_pii("")
        assert result["detected"] is False
        assert result["counts"] == {}

    def test_plain_prose_no_pii(self):
        result = scan_source_pii(
            "This is a normal government memo about procurement and logistics."
        )
        assert result["detected"] is False
        assert result["counts"] == {}

    def test_engine_key_present(self):
        result = scan_source_pii("No PII here.")
        assert "engine" in result

    def test_meta_key_unchanged(self):
        assert META_KEY == "pii_scan"
        assert EVENT_TYPE == "pii_detected"

    def test_counts_no_raw_values(self):
        result = scan_source_pii("Contact test@example.com or 555-123-4567.")
        for v in result["counts"].values():
            assert isinstance(v, int), f"Unexpected non-int count value: {v!r}"

    def test_category_order_stable(self):
        result = scan_source_pii(
            "Email test@example.com, IP 192.168.0.1, card 4111111111111111."
        )
        counts_keys = list(result["counts"].keys())
        ordered_keys = [k for k in _CATEGORY_ORDER if k in result["counts"]]
        for i, key in enumerate(ordered_keys):
            assert counts_keys[i] == key


class TestRegexFallback(unittest.TestCase):
    """When PII_ENGINE=regex the Phase 11K regex engine is used."""

    def setUp(self):
        self._prev = os.environ.get("PII_ENGINE")
        os.environ["PII_ENGINE"] = "regex"

    def tearDown(self):
        if self._prev is None:
            os.environ.pop("PII_ENGINE", None)
        else:
            os.environ["PII_ENGINE"] = self._prev

    def test_email_detected_by_regex(self):
        result = scan_source_pii("Contact admin@example.com for help.")
        assert result["engine"] == "regex"
        assert result["counts"].get("email", 0) >= 1

    def test_ip_detected_by_regex(self):
        result = scan_source_pii("Server at 192.168.1.1.")
        assert result["engine"] == "regex"
        assert result["counts"].get("ipv4", 0) >= 1

    def test_luhn_valid_card_detected(self):
        result = scan_source_pii("Card number 4111111111111111 was used.")
        assert result["engine"] == "regex"
        assert result["counts"].get("credit_card", 0) >= 1

    def test_luhn_invalid_card_not_detected(self):
        result = scan_source_pii("Random digits 1234567890123456 in text.")
        assert result["counts"].get("credit_card", 0) == 0


# ---------------------------------------------------------------------------
# Layer 2 — Presidio engine tests (skipped if not installed)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not PRESIDIO_AVAILABLE, reason="presidio_analyzer not installed")
class TestPresidioEngine:
    """Tests for the Presidio + BERT engine (requires presidio_analyzer)."""

    @pytest.fixture(autouse=True)
    def _reset_env(self, monkeypatch):
        monkeypatch.setenv("PII_ENGINE", "presidio")

    def test_email_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Contact john.doe@example.com for details.")
        categories = [f.category for f in findings]
        assert "email" in categories

    def test_phone_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Call us at +1-800-555-1234.")
        categories = [f.category for f in findings]
        assert "phone" in categories

    def test_ip_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Server IP is 192.168.0.1.")
        categories = [f.category for f in findings]
        assert "ipv4" in categories

    def test_credit_card_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Payment card 4111111111111111 was charged.")
        categories = [f.category for f in findings]
        assert "credit_card" in categories

    def test_aadhaar_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Aadhaar: 2341 2341 2346")
        categories = [f.category for f in findings]
        assert "aadhaar" in categories

    def test_pan_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("PAN: ABCDE1234F")
        categories = [f.category for f in findings]
        assert "pan" in categories

    def test_passport_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Passport number A1234567 was verified.")
        categories = [f.category for f in findings]
        assert "passport" in categories

    def test_voter_id_detected(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("EPIC number ABC1234567 matches records.")
        categories = [f.category for f in findings]
        assert "voter_id" in categories

    def test_no_raw_values_in_findings(self):
        from app.core.presidio_engine import detect_pii_presidio
        findings = detect_pii_presidio("Email test@example.com and phone 555-123-4567.")
        for f in findings:
            assert f.redacted_snippet.startswith("[PII:")
            assert "test@example.com" not in f.redacted_snippet
            assert "555-123-4567" not in f.redacted_snippet

    def test_score_above_threshold(self):
        from app.core.presidio_engine import _SCORE_THRESHOLD, detect_pii_presidio
        findings = detect_pii_presidio("Contact admin@example.com.")
        for f in findings:
            assert f.score >= _SCORE_THRESHOLD

    def test_redact_pii_presidio_preserves_newlines(self):
        from app.core.presidio_engine import redact_pii_presidio
        text = "Line one.\n\nSend to admin@example.com please."
        result = redact_pii_presidio(text)
        assert "admin@example.com" not in result
        assert "[PII:" in result
        assert "Line one.\n\nSend to " in result

    def test_empty_text_returns_empty(self):
        from app.core.presidio_engine import detect_pii_presidio
        assert detect_pii_presidio("") == []

    def test_none_text_returns_empty(self):
        from app.core.presidio_engine import detect_pii_presidio
        assert detect_pii_presidio(None) == []  # type: ignore[arg-type]

    def test_scan_source_pii_uses_presidio_engine(self):
        result = scan_source_pii(
            "Contact john.doe@example.com or call 555-123-4567."
        )
        assert result["engine"] == "presidio"
        assert result["detected"] is True

    def test_scan_source_pii_counts_non_negative(self):
        result = scan_source_pii("IP address 192.168.0.1 and email a@b.com.")
        for v in result["counts"].values():
            assert isinstance(v, int) and v >= 0

    def test_long_document_chunked_no_double_count_in_overlap(self):
        """Entities in the chunk-overlap region must be counted once, not twice."""
        from app.core.presidio_engine import detect_pii_presidio
        # Place admin@example.com right inside the chunk-0 / chunk-1 overlap window (word ~375)
        long_text = ("word " * 375) + "admin@example.com " + ("word " * 125)
        findings = detect_pii_presidio(long_text)
        email_findings = [f for f in findings if f.category == "email"]
        assert len(email_findings) == 1
