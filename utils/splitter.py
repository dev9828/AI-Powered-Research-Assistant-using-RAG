from typing import List

from langchain_core.documents import Document


def split_text(docs: List[Document], chunk_size: int = 1000, chunck_overlap: int = 200) -> List[Document]:
    """Simple character-based splitter that avoids optional spaCy dependency."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunck_overlap >= chunk_size:
        raise ValueError("chunck_overlap must be smaller than chunk_size")

    chunks: List[Document] = []

    for doc in docs:
        text = getattr(doc, "page_content", "") or ""
        metadata = getattr(doc, "metadata", {}) or {}

        start = 0
        step = chunk_size - chunck_overlap
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append(Document(page_content=chunk_text, metadata=metadata))
            start += step

    return chunks
