import json
import os
from datetime import datetime

from whitebox_hallucinations.generation.decoding import generate_answer
from whitebox_hallucinations.wbh_datasets.loaders.base_loader import load_jsonl

DATA_PATH = "src/whitebox_hallucinations/wbh_datasets/processed/sample_qa.jsonl"


def run():
    data = load_jsonl(DATA_PATH)

    run_name = (
        f"baseline_sample_decoding_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    )
    out_dir = f"experiments/{run_name}"
    os.makedirs(out_dir, exist_ok=True)

    out_path = f"{out_dir}/predictions.jsonl"

    with open(out_path, "w") as f:
        for item in data:
            answer = generate_answer(item["question"])

            record = {
                "id": item["id"],
                "question": item["question"],
                "context": item["context"],
                "model_answer": answer,
                "reference_answer": item["reference_answer"],
                "confidence": None,
                "decoding_params": {"temperature": 0.0, "top_p": 1.0, "top_k": 0},
                "metadata": {
                    "model_name": "dummy-baseline",
                    "run_name": run_name,
                    "timestamp": datetime.now().isoformat(),
                },
            }

            f.write(json.dumps(record) + "\n")

    print("Saved:", out_path)


def main():
    run()


if __name__ == "__main__":
    main()
