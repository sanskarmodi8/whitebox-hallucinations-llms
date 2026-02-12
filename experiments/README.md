# Experiment Output Format

Every experiment run must produce a JSONL file:

predictions.jsonl

Each line represents one evaluated sample.

Schema:

{
  "id": str,
  "question": str,
  "context": str | null,
  "model_answer": str,
  "reference_answer": str | null,
  "confidence": float | null,
  "decoding_params": {
    "temperature": float,
    "top_p": float,
    "top_k": int
  },
  "metadata": {
    "model_name": str,
    "run_name": str,
    "timestamp": str
  }
}

Run naming format:

<model>_<dataset>_<intervention>_<timestamp>

Example:
mistral_squad_decoding_2026-02-12
