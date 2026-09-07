"""Provider-agnostic LLM adapter.

Configured via backend/.env (loaded by env_config):
  ANTHROPIC_API_KEY  (Claude)
  OPENAI_API_KEY     (OpenAI or Azure OpenAI v1 endpoint via OPENAI_BASE_URL)
  LLM_MODEL          (default gpt-5-mini; reasoning models use max_completion_tokens)

Without a key everything still works via the deterministic fallback generator.
"""
import json
import os

import httpx

import env_config  # noqa: F401  (loads .env)


class LLMUnavailable(Exception):
    pass


def get_openai_auth() -> tuple:
    return os.environ["OPENAI_API_KEY"], os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")


def _call_anthropic(prompt: str, max_tokens: int = 4000) -> str:
    key = os.environ["ANTHROPIC_API_KEY"]
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={
            "model": os.environ.get("LLM_MODEL", "claude-sonnet-4-20250514"),
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def _call_openai(prompt: str, max_tokens: int = 4000) -> str:
    key, base = get_openai_auth()
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    # gpt-5* reasoning models reject max_tokens/temperature — use max_completion_tokens
    if model.startswith("gpt-5") or model.startswith("o"):
        body["max_completion_tokens"] = max_tokens
    else:
        body["max_tokens"] = max_tokens
        body["temperature"] = 0.7
    resp = httpx.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
        json=body,
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def llm_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))


def generate(prompt: str, max_tokens: int = 4000) -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return _call_anthropic(prompt, max_tokens)
    if os.environ.get("OPENAI_API_KEY"):
        return _call_openai(prompt, max_tokens)
    raise LLMUnavailable("No LLM API key configured")


KNOWLEDGE_QUIZ_PROMPT = """You are a subject-matter examiner for India's capacity-building programmes.
Write {n} multiple-choice questions for the course/module described below in English, at a mix of difficulty levels
"L1" (easy/recall), "L2" (medium/applied) and "L3" (hard/analytical) — roughly 2 L1, 2 L2, 1 L3 for 5 questions;
scale proportionally for other counts. All questions and options must be in clear English. For each question, set "area" to the CLOSEST match from: {areas}.
Return STRICT JSON: a list of objects with fields:
question, options (exactly 4 strings), correct_index (0-3), explanation, area, level.
Only include well-established, verifiable facts in your questions. Vary the position of the correct answer.

Course/module description:
{context}
"""


QUIZ_PROMPT = """You are a subject-matter question-setter for India's capacity-building programmes.
Using ONLY the context below, write {n} multiple-choice questions in clear English at Bloom's taxonomy level: {level}.
Return STRICT JSON: a list of objects with fields:
question, options (exactly 4 strings), correct_index (0-3), explanation, source_snippet, area (short competency area label), difficulty (easy|medium|hard).
Do not introduce facts not present in the context. Vary the position of the correct answer.

Context:
{context}
"""


def parse_llm_quiz(raw: str) -> list:
    """Extract the JSON list from an LLM response (tolerates code fences)."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    start, end = raw.find("["), raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON array in LLM response")
    items = json.loads(raw[start:end + 1])
    out = []
    for q in items:
        if not all(k in q for k in ("question", "options", "correct_index")):
            continue
        if len(q["options"]) != 4 or not (0 <= q["correct_index"] <= 3):
            continue
        out.append({
            "id": f"llm_{abs(hash(q['question'])) % 10**8}",
            "question": q["question"],
            "options": q["options"],
            "answer": q["correct_index"],
            "explanation": q.get("explanation", ""),
            "source_snippet": q.get("source_snippet", ""),
            "area": q.get("area", "Uploaded Material"),
            "difficulty": q.get("difficulty", q.get("level", "medium")),
            **({"level": q["level"]} if q.get("level") else {}),
        })
    return out
