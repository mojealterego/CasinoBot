"""Deterministic discrete-event digital twin for offline deployment gates.

No containers, ROS, accelerated wall-clock physics, or FPGA programming.
All events are synthetic and bounded; candidate plans never execute code.
"""
from heapq import heappop, heappush
from math import isfinite


def simulate(events, *, initial_capacity=10, max_events=10000,
             max_virtual_time=1000000):
    """Process (time, load_delta) events and report first capacity violation."""
    if type(initial_capacity) is not int or initial_capacity < 0:
        raise ValueError("capacity must be a nonnegative integer")
    if type(max_events) is not int or not 1 <= max_events <= 100000:
        raise ValueError("invalid event bound")
    if type(max_virtual_time) is not int or max_virtual_time < 0:
        raise ValueError("invalid virtual-time bound")
    if len(events) > max_events:
        raise ValueError("event budget exceeded")
    heap = []
    for i, event in enumerate(events):
        if not isinstance(event, (tuple, list)) or len(event) != 2:
            raise ValueError("events must be (time, delta) pairs")
        time, delta = event
        if type(time) is not int or time < 0 or time > max_virtual_time:
            raise ValueError("invalid virtual time")
        if type(delta) is not int:
            raise ValueError("load delta must be an integer")
        heappush(heap, (time, i, delta))
    load, peak, processed = 0, 0, 0
    while heap:
        time, _, delta = heappop(heap)
        load += delta
        processed += 1
        peak = max(peak, load)
        if load < 0 or load > initial_capacity:
            return {"status": "rejected", "time": time, "load": load,
                    "peak_load": peak, "processed": processed,
                    "reason": "capacity_or_underflow"}
    return {"status": "accepted", "time": None, "load": load,
            "peak_load": peak, "processed": processed, "reason": "within_bounds"}


def compare_candidate(baseline_events, candidate_events, *, capacity,
                      max_events=10000):
    """Require both baseline and candidate to pass; no deployment side effects."""
    baseline = simulate(baseline_events, initial_capacity=capacity, max_events=max_events)
    candidate = simulate(candidate_events, initial_capacity=capacity, max_events=max_events)
    return {"baseline": baseline, "candidate": candidate,
            "promotion_eligible": baseline["status"] == "accepted"
            and candidate["status"] == "accepted"}
