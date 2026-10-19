"""Validate the existing Markdown RAG source without changing its format or requiring models."""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAG_FILE = BASE_DIR / "rag_documents" / "Vortiq_RAG_Knowledge_Base.md"

def main():
    if not RAG_FILE.exists():
        raise FileNotFoundError(f"RAG document not found: {RAG_FILE}")
    text = RAG_FILE.read_text(encoding="utf-8")
    sections = [s.strip() for s in re.split(r"(?=^### Record \d+:)", text, flags=re.MULTILINE) if s.strip()]
    if not sections and text.strip():
        sections = [text.strip()]
    codes = []
    for section in sections:
        m = re.search(r"(?im)^\\s*(?:[-*]\\s*)?(?:\\*\\*)?Alarm code:(?:\\*\\*)?\\s*([^\\s`*]+)", section)
        if m:
            codes.append(m.group(1).strip("*` "))
    print("Vortiq model-free RAG validation")
    print("Source:", RAG_FILE.name)
    print("Sections:", len(sections))
    print("Sections with explicit alarm-code fields:", len(codes))
    print("Unique alarm codes:", len(set(c.upper() for c in codes)))
    print("No embeddings or vector index were created. Existing RAG source format was not modified.")

if __name__ == "__main__":
    main()
