"""Offline retrospective failure attribution over bounded decision traces.

No retrocausality or neural backpropagation. Earlier recorded decisions
receive penalties for future candidate ranking, never rewriting history.
"""


def retrospective_penalties(trace, *, failure_index, decay=0.5, max_steps=1000):
    """Assign geometrically decaying penalties to decisions before failure."""
    if type(max_steps) is not int or not 1 <= max_steps <= 100000:
        raise ValueError("invalid trace bound")
    steps = tuple(trace)
    if not steps or len(steps) > max_steps or any(not isinstance(s, str) or not s
                                                 for s in steps):
        raise ValueError("bounded nonempty decision labels required")
    if type(failure_index) is not int or not 0 <= failure_index < len(steps):
        raise ValueError("failure index out of range")
    if type(decay) not in (int, float) or not 0 < decay <= 1:
        raise ValueError("decay must be in (0,1]")
    return [{"decision": steps[i], "index": i,
             "penalty": decay ** (failure_index - i)}
            for i in range(failure_index + 1)]


def penalty_lookup(penalties):
    """Aggregate penalties for repeated labels, without mutating source trace."""
    result = {}
    for item in penalties:
        key = item["decision"]
        result[key] = result.get(key, 0.0) + item["penalty"]
    return result
