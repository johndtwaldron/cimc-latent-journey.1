# CIMC Latent Journey

A “Hero’s Journey as latent space” explorer: search a corpus of semantic atoms, then curate a path to form a journey.

## Demo
![Demo](./demo.gif)

## What it does
- Embeds corpus rows (stage/spoke/act/text/source/workstream/psych_axis)
- Semantic search (Top-K)
- Manual node selection to build a journey
- Journey plot (spoke over steps)
- Export journey as CSV

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py