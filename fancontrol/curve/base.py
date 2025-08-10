import math
from abc import ABC, abstractmethod

from ..tools.constants import PWM_MAX


class Point:
    def __init__(self, temperature: float, pwm: int):
        self._temperature = temperature
        self._pwm = pwm

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def pwm(self) -> int:
        return self._pwm


class Curve(ABC):
    @abstractmethod
    def _convert(self, input: float) -> int:
        pass

    def convert(self, input: float | None) -> int:
        if input is None or input < 0:
            return PWM_MAX
        return self._convert(input)


class PointsCurve(Curve, ABC):
    _points: list[Point]

    def __init__(self):
        self._points = []

    def next(self, point: Point):
        last = self._points[-1] if self._points else None
        if last is None:
            self._points.append(point)
            return

        if last.temperature > point.temperature or last.pwm > point.pwm:
            raise ValueError("new point must be greater or equals than last point")

        if last.temperature == point.temperature and last.pwm == point.pwm:
            raise ValueError("duplicate point added")

        self._points.append(point)
