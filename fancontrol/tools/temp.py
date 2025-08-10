from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

from .fs import try_read_int


class Temp(ABC):
    _index: int
    _name: str
    _device: str

    def __init__(self, index: int, name: str, device: str):
        self._index = index
        self._name = name
        self._device = device

    @property
    @abstractmethod
    def degree(self) -> None | float:
        pass

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        if self._name:
            return self._name
        return f"{self._device}_{self._index}"


class ActiveTemp(Temp):
    _millidegreefile: Path

    def __init__(self, index: int, name: str, device: str, millidegreefile: Path):
        super().__init__(index, name, device)
        self._millidegreefile = millidegreefile

    @property
    def degree(self):
        millidegree = try_read_int(self._millidegreefile, 0)
        if millidegree <= 0:
            return None
        return float(millidegree) / 1000.0


class StaticTemp(Temp):
    _degree: int

    def __init__(self, index: int, name: str, device: str, degree: int):
        super().__init__(index, name, device)
        self._degree = degree
        if degree < 1:
            raise ValueError(f"Invalid temperature value: {degree}")

    @property
    def degree(self):
        return float(self._degree)


type TempList = list[Temp]
