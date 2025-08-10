from .base import Curve, Point, PointsCurve


class Polyline(PointsCurve):
    def _convert(self, input: float) -> int:
        for point in self._points:
            if input < point.temperature:
                return point.pwm
        return 255

class StraightLine(PointsCurve):
    def _convert(self, input: float) -> int:
        if not self._points:
            return 255

        # Find the two points the input is between
        for i in range(len(self._points) - 1):
            p1 = self._points[i]
            p2 = self._points[i + 1]
            if p1.temperature <= input < p2.temperature:
                # Linear interpolation
                return int(p1.pwm + (p2.pwm - p1.pwm) * (input - p1.temperature) / (p2.temperature - p1.temperature))

        # If input is out of bounds, return the closest endpoint
        if input < self._points[0].temperature:
            return self._points[0].pwm
        return self._points[-1].pwm
