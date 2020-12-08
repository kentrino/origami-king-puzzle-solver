import numpy as np

numpy_hash = np.frompyfunc(lambda a, b: a * 2 + b, 2, 1)


def make_hash(a: np.ndarray, items: int):
    return numpy_hash.accumulate(a, dtype=np.object)[items - 1] + 2 ** items


_roll_cache = {}


def roll(ring: np.ndarray, n: int, items: int):
    key = (make_hash(ring, items), n)
    if key not in _roll_cache:
        rolled = np.roll(ring, n)
        _roll_cache[key] = rolled
        return rolled
    return _roll_cache[key]

