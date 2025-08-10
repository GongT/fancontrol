import math
from collections.abc import Iterable
from typing import Sequence

from .temp import Temp

type AcceptType = Temp | None | float


def tempToValue(value: AcceptType, none_is: float | None = None):
    if isinstance(value, Temp):
        return value.degree
    if type(value) is float:
        return value
    if value is None and none_is is not None:
        return none_is

    raise TypeError(f"Invalid temperature type: {type(value)}")


def tempsToValues(values: Sequence[AcceptType]):
    r: list[float] = []
    for value in values:
        if value is None:
            continue
        v = tempToValue(value)
        if v is None or v < 0:
            continue
        r.append(v)

    return r


type CountInput = Sequence[AcceptType | Sequence[AcceptType]]


def _get_values(tempss: CountInput):
    values: list[float] = []
    for temps in tempss:
        if temps is None:
            continue

        if isinstance(temps, Temp):
            v = temps.degree
            if v is None or v < 0:
                continue
            values.append(v)
        elif type(temps) is float or type(temps) is int:
            v = temps
            if v is None or v < 0:
                continue
            values.append(float(v))
        elif isinstance(temps, Iterable):
            values.extend(tempsToValues(temps))
        else:
            raise TypeError(f"Invalid temperature list type: {type(temps)}")
    return values


def average(*tempss: AcceptType | Sequence[AcceptType]):
    values = _get_values(tempss)
    if not values:
        return None
    return sum(values) / len(values)


def maximum(*tempss: AcceptType | Sequence[AcceptType]):
    values = _get_values(tempss)
    if not values:
        return None
    return max(values)


def minimum(*tempss: AcceptType | Sequence[AcceptType]):
    values = _get_values(tempss)
    if not values:
        return None
    return min(values)


class Remember:
    _history: list[float]

    def __init__(self, count=20):
        self._history = []
        self._max = count

    def add(self, value: AcceptType):
        if not value:
            return

        if isinstance(value, Temp):
            v = value.degree
        else:
            v = value

        if v is None or v < 0:
            return

        self._history.append(v)

        if len(self._history) > self._max:
            self._history.pop(0)

    def increasing(self):
        near = self.weightedAverage()
        far = self.average()
        if near is None or far is None:
            return 0
        delta = near - far
        return delta if delta > 0 else None

    def decreasing(self):
        near = self.weightedAverage()
        far = self.average()
        if near is None or far is None:
            return 0
        delta = far - near
        return delta if delta > 0 else None

    def average(self):
        return average(self._history)

    def maximum(self):
        return max(self._history)

    def minimum(self):
        return min(self._history)

    def weightedAverage(self):
        weights = list(range(1, len(self._history) + 1))
        if not weights:
            return 0
        weighted_sum = sum(w * v for w, v in zip(weights, self._history))
        return weighted_sum / sum(weights)
