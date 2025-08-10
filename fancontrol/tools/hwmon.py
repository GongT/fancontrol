import inspect
import re
from pathlib import Path
from typing import Callable

from .constants import sys_root
from .fan import Fan, FanList
from .fs import try_read_int, try_read_txt
from .functions import average, maximum, minimum
from .hddtemp import hddtemp_client
from .temp import ActiveTemp, Temp, TempList


class Controller:
    def __init__(self, name: str, temperatures: TempList, fans: FanList):
        self.name = name
        self.temperatures = temperatures
        self.fans = fans

    def __getitem__(self, item: int):
        return self.temperatures[item]

    def find(self, name: str):
        for temp in self.temperatures:
            if temp.name == name:
                return temp
        return None

    def search(self, search: str):
        r: list[Temp] = []
        for temp in self.temperatures:
            if re.search(search, temp.name):
                r.append(temp)
        return r

    def at(self, index: int):
        return self.temperatures[index] if 0 <= index < len(self.temperatures) else None

    def average(self):
        return average(self.temperatures)

    def maximum(self):
        return maximum(self.temperatures)

    def minimum(self):
        return minimum(self.temperatures)

    def control(self, index: int, value: int):
        index -= 1
        fan = self.fans[index] if 0 <= index < len(self.fans) else None
        if fan:
            fan.control(value)
        else:
            print(f"Fan {index} not found")


_controllers: dict[str, Controller] | None = None


def read_hwmon():
    global _controllers

    if _controllers is not None:
        return _controllers

    new_controllers: dict[str, Controller] = {}
    for dir in sys_root.iterdir():
        if not dir.is_dir():
            continue

        name, temps, fans = init_hwmon(dir)
        if not temps and not fans:
            continue

        if name in new_controllers:
            raise ValueError(f"Duplicate controller found: {name}")

        new_controllers[name] = Controller(name=name, temperatures=temps, fans=fans)

    name = "SATA"
    hdd_temps = hddtemp_client()
    new_controllers[name] = Controller(name=name, temperatures=hdd_temps, fans=[])

    _controllers = new_controllers
    return _controllers


def init_hwmon(dir: Path):
    try:
        device_name = dir.joinpath("name").read_text().strip()
    except:
        device_name = dir.name

    new_temperatures: TempList = []
    new_fans: FanList = []

    for i in range(1, 100):
        pwmfile = dir.joinpath(f"pwm{i}")
        if not pwmfile.exists():
            break

        speedfile = dir.joinpath(f"fan{i}_input")

        fan = Fan(
            index=i,
            device=device_name,
            pwmfile=pwmfile,
            speedfile=speedfile,
        )
        new_fans.append(fan)

    for i in range(1, 100):
        millidegree = dir.joinpath(f"temp{i}_input")
        if not millidegree.exists():
            break

        temp_name = try_read_txt(dir.joinpath(f"temp{i}_label"), f"temp{i}")

        temp = ActiveTemp(
            index=i,
            name=temp_name,
            device=device_name,
            millidegreefile=millidegree,
        )
        new_temperatures.append(temp)

    return device_name, new_temperatures, new_fans


def missing(name):
    print(f'using controller "{name}" is missing from system')
    return Controller(fans=[], temperatures=[], name=name)


def calculate(fn: Callable):
    controllers = read_hwmon()
    kwargs = {}
    for key in inspect.signature(fn).parameters.keys():
        kwargs[key] = controllers.get(key, None) or missing(key)
    fn(**kwargs)


def enter_critical():
    print("enter full speed mode")
    controllers = read_hwmon()
    for device in controllers.values():
        for fan in device.fans:
            fan.disable()
