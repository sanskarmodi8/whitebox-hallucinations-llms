import os
from datasets.loaders.base_loader import load_jsonl

def test_base_loader_sample_file():
    path = os.path.join("datasets", "processed", "sample_qa.jsonl")
    assert os.path.exists(path), "sample_qa.jsonl missing"
    data = load_jsonl(path)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "question" in data[0]
