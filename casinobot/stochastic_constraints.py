"""Exact bounded weighted model counting for independent Boolean variables.

Offline educational solver; not a prediction of random casino outcomes.
"""
from fractions import Fraction
from itertools import product


def weighted_model_count(probabilities, clauses, *, max_variables=16):
    """Return exact P(CNF) for independent Bernoulli variables.

    Variables are numbered 1..n; each clause is an OR of signed literals.
    Empty CNF is true; an empty clause is false. Fractions avoid float drift.
    """
    ps = tuple(probabilities)
    if type(max_variables) is not int or not 0 <= max_variables <= 20:
        raise ValueError('invalid variable limit')
    if len(ps) > max_variables:
        raise ValueError('variable limit exceeded')
    if any(type(p) is not Fraction or not 0 <= p <= 1 for p in ps):
        raise ValueError('probabilities must be Fractions in [0,1]')
    cs = tuple(tuple(clause) for clause in clauses)
    if any(type(lit) is not int or lit == 0 or abs(lit) > len(ps)
           for clause in cs for lit in clause):
        raise ValueError('invalid CNF literal')
    total = Fraction(0)
    satisfying = 0
    for bits in product((False, True), repeat=len(ps)):
        if all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
               for clause in cs):
            weight = Fraction(1)
            for bit, p in zip(bits, ps):
                weight *= p if bit else 1-p
            total += weight
            satisfying += 1
    return {'probability': total, 'satisfying_assignments': satisfying,
            'assignments_examined': 1 << len(ps), 'variables': len(ps)}
