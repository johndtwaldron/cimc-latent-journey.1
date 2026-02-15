Perfect — if it’s running on Streamlit Cloud now, you’re in “package + present” mode.

Here’s a tight write-up you can drop straight into README.md and your GitHub Pages docs/index.md (same content, slightly different headers). It hits their four bullets cleanly.

⸻

CIMC Latent Journey

A small interactive explorer that treats the Hero’s Journey / individuation as a latent space. You search a corpus of “semantic atoms,” then curate nodes into a path. The app plots your selections as a journey curve and exports the result as CSV.

What it does (Functional solution)
	•	Loads a corpus CSV of short “semantic atoms” annotated with:
	•	stage (canonical journey stage)
	•	spoke (wheel / sub-dimension)
	•	act (departure / initiation / return)
	•	source (debug provenance: Matrix, Fight Club, etc.)
	•	workstream (optional: lmb/career/dating/spiritual/fitness/story)
	•	psych_axis (tension pair: e.g. comfort_vs_truth)
	•	Performs semantic search over the corpus (Top-K results).
	•	Lets the user pick nodes to form a journey.
	•	Visualizes the journey as a Journey Map (spoke value over path steps).
	•	Exports the chosen journey as a CSV artifact (reproducible, shareable).

Why it’s interesting (Clear thinking + creative approach)

This project reframes narrative transformation as something you can navigate:
	•	Each atom is story-agnostic: a compact psychological beat (“Truth hurts”, “Own your shadow”, “Choose presence”).
	•	Story labels (source) exist mainly for debugging and provenance; the core object is the atom and its metadata.
	•	The goal is to see whether diverse stories still form the same underlying topology of change when embedded.

Key design choices + tradeoffs (Thoughtful decisions)

1) “User-curated path” instead of automatic story generation

Choice: user selects nodes manually.
Tradeoff: less automation, more interpretability.
Reason: the artifact is meant to be auditable (you can see what you selected and why), and it avoids hallucinated narrative glue.

2) Lightweight schema over heavy ontology

Choice: a small fixed schema (stage/spoke/act/psych_axis) rather than a complex taxonomy.
Tradeoff: less expressive, but faster iteration and clearer debugging.

3) Precomputed embeddings for stable hosted demos

Choice: embeddings are computed locally and stored as data/embeddings.npy.
Tradeoff: small repo size increase, but hosted reliability improves dramatically (no slow/fragile runtime embedding step).

4) Provenance labels are “debug tools,” not the model’s truth

Choice: keep source as provenance only; don’t treat it as the semantic core.
Tradeoff: requires discipline in data entry, but preserves the “journey is universal” hypothesis.

Process & reproducibility (Well-documented)

Data
	•	Corpus lives at: data/corpus.csv
	•	Embeddings live at: data/embeddings.npy

Run locally

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py

Hosted demo

Deployed via Streamlit Community Cloud from this repo/branch.

How to add new atoms safely
	1.	Add rows to data/corpus.csv
	2.	Recompute embeddings:

python -m src.embed

	3.	Commit updated corpus.csv + embeddings.npy

Known limitations / next steps
	•	Add a UMAP/t-SNE visualization of the full corpus embedding space.
	•	Add filters by workstream and/or psych_axis.
	•	Add dedupe checks and coverage metrics to prevent “mushy” samey entries.
	•	Expand somatic atoms to better represent nervous system language (freeze/flight/etc.).

⸻

What you should do tonight (minimum viable polish)
	1.	Put that write-up into README.md.
	2.	Copy a shorter version into docs/index.md (Pages).
	3.	Add:
	•	One GIF/screenshot of the UI
	•	One example exported journey CSV (you already have exports)

If you paste your current README.md, I’ll rewrite it in-place with this structure and keep your existing bits that matter.