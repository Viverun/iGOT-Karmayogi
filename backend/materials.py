"""Upload ingestion + grounded MCQ generation from uploaded material."""
import re

from llm import generate, llm_available, QUIZ_PROMPT, parse_llm_quiz, LLMUnavailable


def extract_text(filename: str, raw: bytes) -> str:
    """PDF via pypdf if available; plain text otherwise."""
    if filename.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(raw))
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception:
            raise ValueError("Could not extract PDF text (is pypdf installed?)")
    return raw.decode("utf-8", errors="ignore")


def chunk_text(text: str, size: int = 1200) -> list:
    chunks, buf = [], []
    length = 0
    for para in re.split(r"\n\s*\n", text):
        if length + len(para) > size and buf:
            chunks.append("\n\n".join(buf))
            buf, length = [], 0
        buf.append(para.strip())
        length += len(para)
    if buf:
        chunks.append("\n\n".join(buf))
    return [c for c in chunks if len(c.strip()) > 80]


def _fallback_quiz(chunks: list, n: int) -> list:
    """No-key fallback: sentence-completion MCQs mined from the material."""
    questions = []
    for chunk in chunks:
        for sent in re.split(r"(?<=[.!?])\s+", chunk):
            sent = sent.strip()
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-']{4,}", sent)
                     if w[0].isupper() or w.islower()]
            if len(sent) < 60 or len(words) < 8:
                continue
            target = max(words, key=len)
            stem = sent.replace(target, "______", 1)
            distractors = [w for w in set(words) if w != target][:3]
            while len(distractors) < 3:
                distractors.append("None of the above")
            options = distractors + [target]
            questions.append({
                "id": f"fb_{abs(hash(sent)) % 10**8}",
                "question": f"Fill in the blank per the material: \"{stem}\"",
                "options": options,
                "answer": len(distractors),
                "explanation": "Directly stated in the uploaded material.",
                "source_snippet": sent[:180],
                "area": "Uploaded Material",
                "difficulty": "easy",
            })
            if len(questions) >= n:
                return questions
    return questions


def generate_quiz_from_material(text: str, n: int = 5, level: str = "Understand",
                                focus_query: str | None = None,
                                material_id: int | None = None) -> tuple[list, str, list]:
    """Returns (questions, generator, used_chunks).

    With an LLM key: retrieves the chunks most relevant to focus_query (the
    user's weakest competency areas, embedded via Pinecone) and grounds
    generation strictly in them. Falls back to mined MCQs otherwise.
    """
    chunks = chunk_text(text)
    try:
        import vector_store
        if focus_query:
            hits = vector_store.query_similar_chunks(focus_query, top_k=6, material_id=material_id)
            used = [h["text"] for h in hits] or chunks[:6]
        else:
            used = chunks[:6]
        if llm_available():
            raw = generate(QUIZ_PROMPT.format(n=n, level=level, context="\n\n---\n\n".join(used)))
            questions = parse_llm_quiz(raw)
            if questions:
                return questions[:n], "llm", used
    except Exception:
        pass
    return _fallback_quiz(chunks, n), "fallback", chunks[:2]
