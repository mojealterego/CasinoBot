"""Small deterministic sparse dictionary learner for offline feature audits.

Linear nonnegative sparse coding with projected gradient steps and L1 penalty.
Not a trained LLM SAE, nor proof that features are monosemantic.
"""
from math import isfinite, sqrt


def _matrix(rows, name):
    rows = tuple(tuple(row) for row in rows)
    if not rows or not rows[0] or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError(f"{name}: nonempty rectangular matrix required")
    if any(type(x) not in (float, int) or not isfinite(x) for r in rows for x in r):
        raise ValueError(f"{name}: finite numeric values required")
    return rows


def sparse_encode(activations, dictionary, *, l1=0.1, steps=100, rate=0.05):
    """Encode rows X with fixed dictionary D (features x dimensions).

    Minimizes approximately 0.5||X-ZD||^2 + l1*sum(Z), with Z>=0.
    """
    xs, ds = _matrix(activations, "activations"), _matrix(dictionary, "dictionary")
    if len(xs[0]) != len(ds[0]):
        raise ValueError("activation and dictionary dimensions differ")
    if not isfinite(l1) or l1 < 0 or not isfinite(rate) or rate <= 0:
        raise ValueError("invalid optimization hyperparameters")
    if type(steps) is not int or not 1 <= steps <= 10000:
        raise ValueError("steps must be in [1,10000]")
    if any(sum(x*x for x in d) == 0 for d in ds):
        raise ValueError("dictionary atoms must be nonzero")
    codes = []
    for x in xs:
        z = [0.0] * len(ds)
        for _ in range(steps):
            reconstruction = [sum(z[j]*ds[j][k] for j in range(len(ds)))
                              for k in range(len(x))]
            residual = [reconstruction[k]-x[k] for k in range(len(x))]
            z = [max(0.0, z[j]-rate*(sum(residual[k]*ds[j][k]
                                        for k in range(len(x)))+l1))
                 for j in range(len(ds))]
        codes.append(tuple(z))
    return tuple(codes)


def reconstruction_metrics(activations, dictionary, codes, *, threshold=1e-8):
    xs, ds, zs = (_matrix(activations, "activations"),
                  _matrix(dictionary, "dictionary"), _matrix(codes, "codes"))
    if len(xs) != len(zs) or len(xs[0]) != len(ds[0]) or len(zs[0]) != len(ds):
        raise ValueError("shape mismatch")
    if not isfinite(threshold) or threshold < 0:
        raise ValueError("invalid threshold")
    errors = []
    active = 0
    for x, z in zip(xs, zs):
        prediction = [sum(z[j]*ds[j][k] for j in range(len(ds)))
                      for k in range(len(x))]
        errors.extend((a-b)**2 for a, b in zip(x, prediction))
        active += sum(abs(v) > threshold for v in z)
    return {"mse": sum(errors)/len(errors),
            "mean_active_features": active/len(xs),
            "feature_count": len(ds),
            "samples": len(xs)}
