import re
from typing import List, Optional, Tuple

import numpy as np

# lazy import for sentence-transformers
_EMBED_MODEL = None


def _get_embed_model():
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError(
                "sentence-transformers required for scorer: pip install sentence-transformers"
            ) from e
        _EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _EMBED_MODEL


_SENT_SPLIT_RE = re.compile(r"(?<=[\.\?\!])\s+")


def extract_claims(text: str) -> List[str]:
    if not text:
        return []
    sents = [s.strip() for s in _SENT_SPLIT_RE.split(text) if s.strip()]
    return sents


def best_support_score(claim: str, contexts: List[str]) -> float:
    if not contexts:
        return 0.0
    model = _get_embed_model()
    claim_emb = model.encode(claim, convert_to_tensor=True)
    ctx_embs = model.encode(contexts, convert_to_tensor=True)
    from sentence_transformers import util

    sims = util.cos_sim(claim_emb, ctx_embs).cpu().numpy().flatten()
    if sims.size == 0:
        return 0.0
    return float(np.max(sims))


def is_claim_supported(
    claim: str, contexts: List[str], threshold: float = 0.65
) -> bool:
    score = best_support_score(claim, contexts)
    return score >= threshold


def score_answer_ucr(
    model_answer: str, context: Optional[str], threshold: float = 0.65
) -> Tuple[float, int, int]:
    """
    Returns (ucr, unsupported_count, total_claims)
    """
    claims = extract_claims(model_answer)
    if not claims:
        return 0.0, 0, 0
    contexts = [context] if context and context.strip() else []
    unsupported = 0
    for cl in claims:
        if not is_claim_supported(cl, contexts, threshold=threshold):
            unsupported += 1
    ucr = unsupported / len(claims)
    return float(ucr), int(unsupported), int(len(claims))


def faithfulness_score(model_answer: str, context: Optional[str]) -> float:
    claims = extract_claims(model_answer)
    if not claims:
        return 1.0
    contexts = [context] if context and context.strip() else []
    scores = [best_support_score(c, contexts) for c in claims]
    return float(sum(scores) / len(scores))
