def unsupported_claim(model_answer: str, context: str | None) -> bool:
    """
    Placeholder metric.
    Returns True if answer likely contains hallucination.
    Later replaced with real evaluation.
    """
    if context is None:
        return False
    return len(model_answer) > 3 * len(context)
