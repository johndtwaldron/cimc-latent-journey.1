import pandas as pd
import numpy as np
import streamlit as st

from src.config import CORPUS_PATH
from src.embed import embed_texts
from src.search import top_k

st.set_page_config(page_title="Latent Journey (CIMC Challenge)", layout="wide")
st.title("Latent Journey — tiny prototype")

df = pd.read_csv(CORPUS_PATH)
texts = df["text"].tolist()

# TEMP embeddings so the UI runs tonight
vecs = embed_texts(texts)

if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "path" not in st.session_state:
    st.session_state.path = [0]

left, right = st.columns([1, 2])

with left:
    st.subheader("Current position")
    cur = st.session_state.current_idx
    st.write(f"**Stage:** {df.loc[cur,'stage']}")
    st.write(df.loc[cur,'text'])

    if st.button("Reset"):
        st.session_state.current_idx = 0
        st.session_state.path = [0]
        st.rerun()

with right:
    st.subheader("Next steps (nearest neighbours)")
    cur = st.session_state.current_idx
    idxs, sims = top_k(vecs, vecs[cur], k=5, exclude_idx=cur)

    for i, (idx, sim) in enumerate(zip(idxs, sims)):
        cols = st.columns([0.15, 0.85])
        if cols[0].button(f"Go {i+1}", key=f"go_{idx}"):
            st.session_state.current_idx = int(idx)
            st.session_state.path.append(int(idx))
            st.rerun()
        cols[1].write(f"**{df.loc[idx,'stage']}** — {df.loc[idx,'text']}  \n(sim={float(sim):.3f})")

    st.divider()
    st.subheader("Journey so far")
    for step, idx in enumerate(st.session_state.path, start=1):
        st.write(f"{step}. [{df.loc[idx,'stage']}] {df.loc[idx,'text']}")