"""
Simple RAG (retrieval) for FitLife AI.

- Reads .md / .txt files from the knowledge/ folder
- Splits them into sections (chunks)
- Ranks chunks against a question with BM25
- Needs no extra packages and no internet

To use embeddings later (better meaning-based search), replace
KnowledgeBase.search() with a vector store such as Chroma or FAISS.
The rest of the project does not need to change.
"""

import math
import re
from collections import Counter
from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "be", "do", "does", "how", "what", "which", "i", "my",
    "me", "can", "should", "much", "many", "it", "this", "that", "at",
    "by", "from", "as", "if", "you", "your", "about", "per", "day"
}

MAX_CHUNK_CHARS = 900

# At least this share of the question's words must appear in a chunk
MIN_TERM_COVERAGE = 0.5


def tokenize(text):

    words = re.findall(r"[a-z0-9]+", text.lower())

    tokens = []

    for word in words:

        if word in STOPWORDS:
            continue

        # very light stemming: protein / proteins, meal / meals
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]

        tokens.append(word)

    return tokens


def split_into_chunks(text, source):
    """Split a markdown file into sections, one chunk per '## ' heading."""

    title = source
    sections = []
    current_heading = ""
    current_lines = []

    for line in text.splitlines():

        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()

        elif line.startswith("## "):

            if current_lines:
                sections.append((current_heading, current_lines))

            current_heading = line[3:].strip()
            current_lines = []

        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, current_lines))

    chunks = []

    for heading, lines in sections:

        body = "\n".join(lines).strip()

        if not body:
            continue

        # split very long sections by paragraph
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

        parts = []
        buffer = ""

        for paragraph in paragraphs:

            if buffer and len(buffer) + len(paragraph) > MAX_CHUNK_CHARS:
                parts.append(buffer)
                buffer = paragraph
            else:
                buffer = (buffer + "\n\n" + paragraph).strip()

        if buffer:
            parts.append(buffer)

        for part in parts:

            chunks.append({
                "source": source,
                "title": f"{title} - {heading}" if heading else title,
                "text": part
            })

    return chunks


def load_chunks(directory=KNOWLEDGE_DIR):

    directory = Path(directory)

    if not directory.exists():
        return []

    chunks = []

    for path in sorted(directory.iterdir()):

        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        text = path.read_text(encoding="utf-8")

        chunks.extend(split_into_chunks(text, path.name))

    return chunks


class KnowledgeBase:

    K1 = 1.5
    B = 0.75

    def __init__(self, directory=KNOWLEDGE_DIR):

        self.chunks = load_chunks(directory)

        self.doc_tokens = [
            tokenize(chunk["title"] + " " + chunk["text"])
            for chunk in self.chunks
        ]

        self.doc_counts = [Counter(tokens) for tokens in self.doc_tokens]

        self.doc_lengths = [len(tokens) for tokens in self.doc_tokens]

        total = len(self.doc_lengths)

        self.avg_length = (sum(self.doc_lengths) / total) if total else 0

        document_frequency = Counter()

        for tokens in self.doc_tokens:
            document_frequency.update(set(tokens))

        self.idf = {
            term: math.log(1 + (total - df + 0.5) / (df + 0.5))
            for term, df in document_frequency.items()
        }

    def search(self, query, top_k=3, min_score=0.5):

        query_terms = tokenize(query)

        if not query_terms or not self.chunks:
            return []

        unique_terms = set(query_terms)

        scored = []

        for index, counts in enumerate(self.doc_counts):

            score = 0.0

            # Skip chunks that match only a small part of the question
            matched = unique_terms.intersection(counts)

            if len(matched) / len(unique_terms) < MIN_TERM_COVERAGE:
                continue

            for term in query_terms:

                if term not in counts:
                    continue

                frequency = counts[term]

                length_norm = (
                    1 - self.B
                    + self.B * self.doc_lengths[index] / self.avg_length
                )

                score += self.idf[term] * (
                    frequency * (self.K1 + 1)
                    / (frequency + self.K1 * length_norm)
                )

            if score >= min_score:
                scored.append((score, index))

        scored.sort(reverse=True)

        return [
            {
                "source": self.chunks[index]["source"],
                "title": self.chunks[index]["title"],
                "text": self.chunks[index]["text"],
                "score": round(score, 2)
            }
            for score, index in scored[:top_k]
        ]


_knowledge_base = None


def get_knowledge_base():
    """Load the knowledge base once and reuse it."""

    global _knowledge_base

    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()

    return _knowledge_base


if __name__ == "__main__":

    kb = get_knowledge_base()

    print("Chunks loaded:", len(kb.chunks))

    for question in [
        "how much protein do I need for muscle gain",
        "too much fibre causes bloating",
        "how long should I rest between sets",
        "vegan vitamin B12",
        "best pizza recipe"
    ]:

        print("\nQ:", question)

        results = kb.search(question)

        if not results:
            print("  (nothing relevant found)")

        for result in results:
            print(f"  [{result['score']}] {result['source']} | {result['title']}")
