import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure project root is on PYTHONPATH so `src` imports work when running `streamlit run app/app.py`
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.search import search  # noqa: E402


st.set_page_config(page_title="CIMC Latent Journey", layout="wide")

# -----------------------------
# Session state
# -----------------------------
if "journey" not in st.session_state:
    # list of dicts: {id, stage, spoke, act, text, score, source, workstream, psych_axis}
    st.session_state.journey = []

if "last_results" not in st.session_state:
    st.session_state.last_results = pd.DataFrame()

if "results_debug" not in st.session_state:
    st.session_state.results_debug = False

if "history_debug" not in st.session_state:
    st.session_state.history_debug = False

if "locked_after_add" not in st.session_state:
    # When True, user must run a new search before adding another node
    st.session_state.locked_after_add = False


def _row_to_dict(row: pd.Series) -> dict:
    # Keep only known columns if present
    keep = [
        "id",
        "stage",
        "spoke",
        "act",
        "text",
        "score",
        "source",
        "workstream",
        "psych_axis",
    ]
    out = {}
    for k in keep:
        if k in row.index:
            v = row[k]
            # Convert numpy types to python scalars for session_state safety
            try:
                out[k] = v.item()  # type: ignore[attr-defined]
            except Exception:
                out[k] = v
    return out


def undo_last() -> None:
    if st.session_state.journey:
        st.session_state.journey.pop()
    # Allow another pick without forcing a new query if they undo
    st.session_state.locked_after_add = False


# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([2.2, 1.0], gap="large")

with left:
    st.title("CIMC Latent Journey")

    st.caption(
        "Search the corpus, then **pick** nodes to build a journey. "
        "The right panel tracks your chosen path."
    )

    query = st.text_input(
        "Query",
        placeholder="e.g., red pill truth / no mind / am I whole?",
        key="query",
    )
    top_k = st.slider("Top K (how many results to show)", 1, 30, 10)

    cols_btn = st.columns([1, 3])
    with cols_btn[0]:
        do_search = st.button("Search", use_container_width=True)

    if do_search and query.strip():
        st.session_state.last_results = search(query.strip(), top_k=top_k)
        st.session_state.locked_after_add = False
        # Reset selection for a fresh query so only one pick is possible
        st.session_state.pop("selected_result_idx", None)

    results = st.session_state.last_results

    if not results.empty:
        st.subheader("Results")

        # Results-first: show just the text to encourage resonance-based picking.
        st.session_state.results_debug = st.toggle(
            "Show result metadata (debug)",
            value=st.session_state.results_debug,
        )

        # Single-pick control (radio) enforces 1 selection per query.
        def _fmt_idx(i: int) -> str:
            try:
                row = results.loc[i]
            except Exception:
                return str(i)

            txt = str(row.get("text", ""))
            txt_one_line = " ".join(txt.split())
            short = (txt_one_line[:110] + "…") if len(txt_one_line) > 110 else txt_one_line

            # Minimal hinting: stage is optional; keep it light.
            stage = str(row.get("stage", "")).strip()
            if stage:
                return f"{short}  —  ({stage})"
            return short

        st.caption("Choose the line that resonates most. Only one node can be added per query.")

        # Default the selection to the first row.
        idx_options = list(results.index)
        default_idx = idx_options[0] if idx_options else None

        selected_idx = st.radio(
            "Pick one result to add",
            options=idx_options,
            index=0,
            format_func=_fmt_idx,
            disabled=st.session_state.locked_after_add,
            key="selected_result_idx",
        )

        c_add, c_clear, c_hint = st.columns([1, 1, 2])
        with c_add:
            if st.button(
                "Add to Journey",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.locked_after_add or (selected_idx is None),
            ):
                item = _row_to_dict(results.loc[selected_idx])

                # De-dupe on id if available
                if "id" in item:
                    existing_ids = {x.get("id") for x in st.session_state.journey}
                    if item["id"] in existing_ids:
                        st.info("That node is already in your journey.")
                    else:
                        st.session_state.journey.append(item)
                        st.session_state.locked_after_add = True
                        st.session_state.last_results = pd.DataFrame()
                        st.session_state.pop("selected_result_idx", None)
                else:
                    st.session_state.journey.append(item)
                    st.session_state.locked_after_add = True
                    st.session_state.last_results = pd.DataFrame()
                    st.session_state.pop("selected_result_idx", None)

                st.rerun()

        with c_clear:
            if st.button("Clear Results", use_container_width=True):
                st.session_state.last_results = pd.DataFrame()
                st.session_state.locked_after_add = False
                st.rerun()

        with c_hint:
            st.caption("Tip: keep Top K around 5–10 for deliberate picks.")
            if st.session_state.locked_after_add:
                st.warning("Node saved. Enter a new query and click Search to continue the journey.")

        if st.session_state.results_debug:
            with st.expander("Raw results table (debug)", expanded=False):
                debug_cols = [
                    c
                    for c in [
                        "id",
                        "stage",
                        "spoke",
                        "act",
                        "text",
                        "source",
                        "workstream",
                        "psych_axis",
                        "score",
                    ]
                    if c in results.columns
                ]
                st.dataframe(
                    results[debug_cols],
                    hide_index=True,
                    use_container_width=True,
                    height=360,
                )

    # Simple “dot map” of the journey so far (proxy for latent space). 
    # For now, we plot step index vs spoke (wheel position).
    if st.session_state.journey:
        st.subheader("Journey Map")
        jdf = pd.DataFrame(st.session_state.journey)
        jdf = jdf.reset_index().rename(columns={"index": "step"})

        if "spoke" in jdf.columns:
            chart_df = jdf[["step", "spoke"]].dropna()
            chart_df = chart_df.set_index("step")
            st.line_chart(chart_df)
            st.caption("Y = spoke (1–12), X = step in your saved journey.")
        else:
            st.info("No 'spoke' column found in journey items yet.")

with right:
    st.subheader("Journey History")

    st.session_state.history_debug = st.toggle(
        "Show journey metadata (debug)",
        value=st.session_state.history_debug,
    )

    if not st.session_state.journey:
        st.info("No nodes saved yet. Search on the left and add results to start a journey.")
    else:
        jdf = pd.DataFrame(st.session_state.journey)

        # Show a tight view for quick scanning
        if st.session_state.history_debug:
            show_cols = [
                c
                for c in [
                    "id",
                    "stage",
                    "spoke",
                    "act",
                    "text",
                    "source",
                    "workstream",
                    "psych_axis",
                ]
                if c in jdf.columns
            ]
        else:
            show_cols = [c for c in ["stage", "text"] if c in jdf.columns]

        st.dataframe(
            jdf[show_cols],
            hide_index=True,
            use_container_width=True,
            height=420,
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Undo last", use_container_width=True):
                undo_last()
                st.rerun()
        with c2:
            if st.button("Clear journey", use_container_width=True):
                st.session_state.journey = []
                st.rerun()

        # Optional export for debugging / later analysis
        st.download_button(
            "Download journey CSV",
            data=jdf.to_csv(index=False).encode("utf-8"),
            file_name="journey.csv",
            mime="text/csv",
            use_container_width=True,
        )