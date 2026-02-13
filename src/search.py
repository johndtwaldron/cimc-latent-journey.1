import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI

from src.config import EMBED_MODEL, CORPUS_PATH, EMBED_PATH


def _cosine_sim_matrix(query_vec: np.ndarray, mat: np.ndarray) -> np.ndarray:
    # normalize
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12)
    return m @ q


def search(query: str, top_k: int = 5) -> pd.DataFrame:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing. Put it in .env")

    if not os.path.exists(EMBED_PATH):
        raise RuntimeError(f"No embeddings found at {EMBED_PATH}. Run: python -m src.embed")

    df = pd.read_csv(CORPUS_PATH)
    emb = np.load(EMBED_PATH)

    client = OpenAI(api_key=api_key)
    q_resp = client.embeddings.create(model=EMBED_MODEL, input=[query])
    q_vec = np.array(q_resp.data[0].embedding, dtype=np.float32)

    sims = _cosine_sim_matrix(q_vec, emb)
    idx = np.argsort(-sims)[:top_k]

    out = df.iloc[idx].copy()
    out["score"] = sims[idx]
    return out.reset_index(drop=True)


if __name__ == "__main__":
    q = "test query"
    print(search(q, top_k=5))