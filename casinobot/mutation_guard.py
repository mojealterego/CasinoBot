"""Bounded model checking for proposed finite-state mutations.

Purely offline transition systems; no execution of generated code.
Exhaustive within the declared finite horizon, not a general termination proof.
"""
from collections import deque


def verify_transition_system(initial, transitions, *, max_depth=20, max_states=10000,
                             forbidden=(), require_termination=False):
    """Explore reachable states and return counterexample paths.

    transitions: mapping state -> iterable of successor states. States are
    hashable strings. Unlisted states are terminal. A cycle reachable within
    the explored graph is rejected when require_termination=True.
    """
    if not isinstance(initial, str) or not initial:
        raise ValueError("initial state must be a nonempty string")
    if type(max_depth) is not int or not 0 <= max_depth <= 1000:
        raise ValueError("invalid depth bound")
    if type(max_states) is not int or not 1 <= max_states <= 100000:
        raise ValueError("invalid state bound")
    if not isinstance(transitions, dict):
        raise ValueError("transitions must be a mapping")
    graph = {}
    for state, successors in transitions.items():
        if not isinstance(state, str) or not state:
            raise ValueError("invalid state")
        if isinstance(successors, (str, bytes)):
            raise ValueError("successors must be a collection")
        children = tuple(successors)
        if any(not isinstance(x, str) or not x for x in children):
            raise ValueError("invalid successor")
        graph[state] = children
    bad = set(forbidden)
    if any(not isinstance(x, str) for x in bad):
        raise ValueError("forbidden states must be strings")
    queue = deque([(initial, (initial,))])
    seen = {initial}
    reachable = {}
    truncated = False
    while queue:
        state, path = queue.popleft()
        if state in bad:
            return {"status": "rejected", "reason": "forbidden_state",
                    "counterexample": list(path), "states": len(seen)}
        children = graph.get(state, ())
        reachable[state] = children
        if len(path) - 1 >= max_depth:
            if children:
                truncated = True
            continue
        for child in children:
            if child not in seen:
                if len(seen) >= max_states:
                    truncated = True
                    continue
                seen.add(child)
                queue.append((child, path + (child,)))
    if truncated:
        return {"status": "inconclusive", "reason": "bounded_search",
                "counterexample": None, "states": len(seen)}
    if require_termination:
        visiting, visited = set(), set()
        def cycle(node):
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            for child in reachable.get(node, ()):
                if cycle(child):
                    return True
            visiting.remove(node)
            visited.add(node)
            return False
        if cycle(initial):
            return {"status": "rejected", "reason": "reachable_cycle",
                    "counterexample": None, "states": len(seen)}
    return {"status": "accepted", "reason": "finite_model_checked",
            "counterexample": None, "states": len(seen)}
