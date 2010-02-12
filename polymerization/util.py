def choose_state(probs, num, default=None):
    """
    Selects a state from probs given an already generated random number.
    """
    for rate, state in probs:
        if num < rate:
            return state

    return default
