from typing import NamedTuple


class Density(NamedTuple):
    loops: float
    rows: float


class ConversionKoefficient(NamedTuple):
    loops_k: float
    rows_k: float
