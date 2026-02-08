import os
import numpy as np

def embed_texts(texts):
    """
    Returns np.array shape (n, d).
    For tonight: placeholder random vectors so the app runs.
    Tomorrow: swap in real embeddings (OpenAI or local).
    """
    rng = np.random.default_rng(42)
    return rng.normal(size=(len(texts), 64)).astype(np.float32)