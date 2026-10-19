"""Exact alarm-code lookup against the existing Markdown RAG source; no model required."""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAG_FILE = BASE_DIR / "rag_documents" / "Vortiq_RAG_Knowledge_Base.md"

def normalize_code(code):
    return re.sub(r"\s+", "", str(code or "").strip()).upper()

def main():
    if not RAG_FILE.exists():
        print("ERROR: RAG source file not found:", RAG_FILE)
        return
    text = RAG_FILE.read_text(encoding="utf-8")
    sections = [s.strip() for s in re.split(r"(?=^### Record \d+:)", text, flags=re.MULTILINE) if s.strip()]
    if not sections and text.strip():
        sections = [text.strip()]
    print("Vortiq exact-code RAG test (no embeddings)")
    print("Sections loaded:", len(sections))
    code = input("Enter exact alarm code (e.g. SV0411): ").strip()
    if not code:
        print("No code entered.")
        return
    matches = []
    for section in sections:
        m = re.search(r"(?im)^\\s*(?:[-*]\\s*)?(?:\\*\\*)?Alarm code:(?:\\*\\*)?\\s*([^\\s`*]+)", section)
        if m and normalize_code(m.group(1).strip("*` ")) == normalize_code(code):
            matches.append(section)
    if not matches:
        print("NO EXACT MATCH. Do not infer from a similar code.")
        return
    print(f"EXACT MATCH: {len(matches)} section(s)")
    for i, section in enumerate(matches, 1):
        print(f"\\n--- Match {i} ---\\n{section}")

if __name__ == "__main__":
    main()
