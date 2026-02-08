import numpy as np

def cosine_sim_matrix(vecs, query):
    vecs_n = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)
    q_n = query / (np.linalg.norm(query) + 1e-9)
    return vecs_n @ q_n

def top_k(vecs, query_vec, k=5, exclude_idx=None):
    sims = cosine_sim_matrix(vecs, query_vec)
    if exclude_idx is not None:
        sims[exclude_idx] = -1.0
    idx = np.argsort(-sims)[:k]
    return idx, sims[idx]