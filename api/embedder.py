import os
from sentence_transformers import SentenceTransformer

CACHE_DIR = os.getenv("HF_HOME", "/app/.cache/huggingface")

model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=CACHE_DIR)

def embed_text(text: str):
    return model.encode(text)


def embed_chunks(chunks: list):
    texts = [text for text, page_nr in chunks]
    embeddings = model.encode(texts)

    output = []

    for (text, page_nr), embedding in zip(chunks, embeddings):
        output.append((
            text,
            embedding,
            page_nr
        ))

    return output