import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src.search import search

st.title("CIMC Latent Journey")

query = st.text_input("Query")
top_k = st.slider("Top K", 1, 20, 5)

if st.button("Search") and query.strip():
    results = search(query, top_k=top_k)
    st.dataframe(results)