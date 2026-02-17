# White-Box Hallucination Study — Experimental Protocol

A controlled, reproducible empirical study of hallucination behavior in large language models (LLMs). We compare three practical intervention classes — inference-time decoding, system-level retrieval, and parameter-efficient fine-tuning (PEFT/LoRA) — and measure their effects on factual reliability, omission, and cost. The methodology, outputs, and reporting conventions below are mandatory for all experiments.

---

## 1 — Scientific claim & testable hypotheses

**Primary hypothesis (paper claim)**
Parameter-efficient fine-tuning (PEFT/LoRA) on small domain-specific datasets reduces the Unsupported-Claim Rate (UCR) more effectively than inference-time decoding changes alone. Decoding hyperparameters (temperature/top-p) reduce certain hallucination subtypes at the cost of higher omission; retrieval grounding reduces hallucinations caused by missing context, subject to retrieval quality.

**Subsidiary hypotheses**

* **H1 (Decoding):** Lower temperature + conservative top-p reduces *fabrication* (made-up claims) but increases *omission* (omitted correct facts).
* **H2 (Retrieval vs PEFT):** Retrieval reduces hallucinations caused by missing evidence; PEFT reduces hallucinations caused by model priors/knowledge gaps.

---

## 2 — What an experiment is (formal definition)

An **experiment** = one controlled model run where exactly one intervention category is changed (inference-time decoding, training-time fine-tuning, or system-level retrieval) and all other variables are fixed. Experiments must be reproducible, documented, and produce machine-readable outputs according to the protocol below.

---

## 3 — Mandatory output format and run naming (immutable)

**Every run MUST produce** a `predictions.jsonl` file (one JSON object per line). Each entry must include at least these fields:

* `id` — unique sample id
* `question` — input prompt
* `context` — provided evidence string or `null`
* `model_answer` — model output text
* `reference_answer` — ground truth or `null`
* `confidence` — optional numeric confidence or `null`
* `decoding_params` — object with explicit `temperature`, `top_p`, `top_k` used
* `metadata` — object with `model_name`, `run_name`, `timestamp`, git commit or config hash

**Run folder naming convention (required):**

```
<model>_<dataset>_<intervention>_<YYYY-MM-DD_HH-MM>
```

Rules:

* Lowercase, underscores, no spaces.
* Timestamps: `YYYY-MM-DD_HH-MM`.
* One intervention type per run (e.g., `decoding`, `lora-r8`, `bm25`).
* Each run folder must contain:

  * `predictions.jsonl` (never edited by hand)
  * `config_used.yaml` (full parameters and dataset path)
  * `run-manifest.json` (git commit, package versions, hardware summary, seed)
  * `metrics.json` (created after scoring)

---

## 4 — Experiment matrix (Phase definitions and variables)

We use a staged approach. Run the listed combinations; start narrow and expand only after Phase 1 is complete and reproducible.

### Phase 1 — Baseline & decoding (minimal, mandatory)

* Model: `google/flan-t5-large` (baseline)
* Decoding grid:

  * `temperature` ∈ {0.0, 0.2, 0.8}
  * `top_p` ∈ {0.9, 1.0}
  * (keep `top_k` = 0)
* Retrieval: none
* Fine-tuning: none

Purpose: validate pipeline, compute primary metric (UCR) across decoding settings.

### Phase 2 — Retrieval & PEFT (builds on Phase 1)

* Retrieval: `none`, `BM25` (lexical), `dense` (sentence embeddings + FAISS)
* PEFT (LoRA): `none`, `rank=8`, `rank=16` (small number of steps; document training config)
* Combine with a subset of decoding settings (choose representative decoding configs from Phase 1)

Purpose: test how retrieval and PEFT individually and jointly affect UCR and omission.

### Phase 3 — Ablations, scaling, and paper experiments

* Extended models (optional): larger models or API-backed models if compute permits
* Larger dataset splits and additional metrics
* Statistical tests, human annotation, final figures and paper drafting

---

## 5 — Datasets (what to use and how to store)

**Storage:** processed files go into `datasets/processed/`; raw downloads go into `datasets/raw/`; processing scripts live in `datasets/loaders/`.

**Phase 1 required datasets (small reproducible subsets)**

1. **SQuAD (factual QA)** — small subset (≈500 samples). Good for measuring unsupported claims and omissions.
2. **FEVER (fact verification)** — small subset (≈200 samples). Good for retrieval-sensitive experiments.
3. **Synthetic hallucination prompts** — curated set (≈200 samples) designed to isolate missing-context vs model-prior failures.

**Format:** Each example must follow the run schema (has `id`, `question`, `context`, `reference_answer`).

**Preparation rules**

* Document preprocessing steps and version of the dataset snapshot.
* Never change a processed snapshot for a published run; create a new processed file and log its name/version.

---

## 6 — Evaluation metrics (definitions and reporting expectations)

**Primary metric**

* **Unsupported-Claim Rate (UCR):** the fraction of claims in model output that are unsupported by the available evidence (context and/or retrieved documents).

**Secondary metrics**

* **Faithfulness score:** average support strength across claims (continuous 0–1).
* **Omission rate:** fraction of ground-truth facts not mentioned by the model when multiple facts exist.
* **Intervention cost:** training GPU-minutes and average inference latency.
* **Human spot-check:** manual verification set (≥20 items per run) to validate automated scoring.

**Metric reporting**

* For every run, produce a `metrics.json` that includes: UCR, faithfulness mean, omission rate, sample counts, and cost stats. Include per-sample breakdowns if feasible (`results/per_sample_*`).
* Report confidence intervals or standard errors where relevant.
* Document thresholds and calibration used for automated scoring (saved in `config_used.yaml`).

---

## 7 — Reproducibility & provenance (strict rules)

* **Baseline run required:** every line of reported analysis must reference a baseline run.
* **Fix random seeds** for training and generation and log them in `run-manifest.json`.
* **Record provenance:** include git commit hash, package versions, and a short hardware summary in each run manifest.
* **No in-place edits:** do not edit `predictions.jsonl` or other run artifacts after creation; create a new run when changing any parameter.
* **Human validation:** attach annotated notes for the human spot-check and record annotator decisions.
* **Archival:** keep run artifacts small and focused; large artifacts may be stored externally but must be linked from the run manifest.

---

## 8 — Team roles & workflow

**Roles**

* **Pipeline owner (Sanskar)** — implement and maintain generation pipeline, orchestrate decoding experiments, push run artifacts, ensure baseline reproducibility.
* **Datasets & retrieval owner (Aryan)** — prepare dataset snapshots, implement and validate BM25/dense retrieval wrappers, produce synthetic prompt generator.
* **Evaluation & analysis owner (Priyanshu)** — implement scorer, calculate metrics, produce plots and statistical analysis, perform human spot-checks.

**Workflow**

* Branch per task: `feat/<name>-<short-task>`.
* Small PRs with a single change; one teammate must review before merge.
* Every merged change must include an update to `run-manifest.json` or `config_used.yaml` if it affects experiments.
* Use labels and issues to coordinate tasks: `data`, `pipeline`, `evaluation`, `paper`, `results`.

---

## 9 — Deliverables by phase (what to produce and commit)

**Phase 1 (required minimum)**

* Baseline run folder: `experiments/<baseline_run>/` with `predictions.jsonl`, `config_used.yaml`, `run-manifest.json`.
* Two additional decoding runs (different temperatures) with analogous artifacts.
* Scoring outputs for all Phase 1 runs: `results/decoding_baseline_scores.json` and per-sample files as needed.
* One figure: UCR vs temperature saved to `results/plots/decoding_vs_ucr.png`.
* One short narrative: `paper/phase1_summary.md` explaining dataset, methods, one result, and limitations.
* Human spot-check file: `paper/human_spotcheck_phase1.md` (20 annotated items).

**Phase 2**

* Retrieval runs and LoRA runs with artifacts and metrics.
* Comparative table and plots: UCR by intervention and cost table (GPU-min).
* Expanded human validation and error analysis (examples that show types of hallucinations).

**Phase 3 (finalization)**

* Statistical analysis, ablations, and final paper figures.
* Paper draft and reproducible artifacts to reproduce every table/figure.
* A short “How to reproduce” document for the repo root describing the exact commands to reproduce figures from run artifacts.

---

## 10 — Reporting, documentation, and commit conventions

* **Commit messages:** use conventional style. Examples:

  * `feat: add model_loader for flan-t5-large`
  * `chore: add decoding config for squad_small`
  * `feat: add UCR scorer`
  * `fix: correct run_name timestamp format`
  * `docs: update experiment protocol`
* **Pull Requests:** include short summary, linked issue, list of changed files, smoke test results.
* **Documentation:** maintain `paper/` with draft figures and `paper/README.md` that explains the contents.
* **Issue tags:** use `data`, `pipeline`, `evaluation`, `experiment`, `paper`.