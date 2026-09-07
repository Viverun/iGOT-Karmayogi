"""PII redaction for anything that reaches a third-party LLM (Anthropic/OpenAI/Gemini).

Design invariant for this codebase: every prompt sent via llm.generate() is built
from department names, competency-area labels, scores and course keys — never
name/email/designation (see gap_engine.py, main.py's _chat_context). The one path
where an officer's own free text reaches the LLM is /api/chat, so that's the only
place PII can leak, and only if the officer types it themselves.
"""
import re

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"(?<!\d)(?:\+?91[-\s]?)?[6-9]\d{9}(?!\d)")
_AADHAAR = re.compile(r"(?<!\d)\d{4}\s?\d{4}\s?\d{4}(?!\d)")
_PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
_NAME_INTRO = re.compile(r"\b(?:[Mm]y name is|[Ii] am|[Ii]'m|[Tt]his is)\s+"
                          r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})")

_REDACTIONS = [
    (_EMAIL, "[REDACTED_EMAIL]"),
    (_AADHAAR, "[REDACTED_ID]"),
    (_PAN, "[REDACTED_ID]"),
    (_PHONE, "[REDACTED_PHONE]"),
]


def redact_pii(text: str) -> str:
    """Strip emails, phone numbers, Aadhaar/PAN-shaped IDs and self-introduced
    names from officer-typed text before it is sent to an external LLM.
    Storage/display to the officer themselves still uses the original text —
    call this only at the point a string is handed to llm.generate()."""
    if not text:
        return text
    out = text
    for pattern, placeholder in _REDACTIONS:
        out = pattern.sub(placeholder, out)
    out = _NAME_INTRO.sub(lambda m: m.group(0).replace(m.group(1), "[REDACTED_NAME]"), out)
    return out
