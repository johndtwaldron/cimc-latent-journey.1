import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from src.config import EMBED_MODEL, CORPUS_PATH, EMBED_PATH


def _get_text_column(df: pd.DataFrame) -> str:
    # pick a sensible default text column
    for c in ["text", "content", "body", "chunk"]:
        if c in df.columns:
            return c
    # fallback: first column
    return df.columns[0]


def embed_corpus(force: bool = False) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing. Put it in .env")

    if (not force) and os.path.exists(EMBED_PATH):
        return f"Embeddings already exist at {EMBED_PATH} (use force=True to overwrite)"

    df = pd.read_csv(CORPUS_PATH)
    if df.empty:
        raise RuntimeError(f"{CORPUS_PATH} is empty")

    text_col = _get_text_column(df)
    texts = df[text_col].astype(str).tolist()

    client = OpenAI(api_key=api_key)

    vectors = []
    # simple batching to avoid giant requests
    batch_size = 128
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        vectors.extend([d.embedding for d in resp.data])

    emb = np.array(vectors, dtype=np.float32)
    os.makedirs(os.path.dirname(EMBED_PATH), exist_ok=True)
    np.save(EMBED_PATH, emb)

    return f"Saved embeddings: {emb.shape} -> {EMBED_PATH}"


if __name__ == "__main__":
    print(embed_corpus())