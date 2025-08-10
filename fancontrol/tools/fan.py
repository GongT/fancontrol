import math
from pathlib import Path

from .constants import PWM_MAX, sys_root
from .fs import try_read_int, try_read_txt


class Fan:
    def __init__(self, index: int, device: str, speedfile: Path, pwmfile: Path):
        self._index = index
        self._device = device
        self._speedfile = speedfile
        self._pwmfile = pwmfile

        self._manual_auto_file = pwmfile.parent.joinpath(f"pwm{index}_enable")

    def initialize(self):
        modefile = self._pwmfile.parent.joinpath(f"pwm{self._index}_mode")
        if try_read_int(modefile, -1) == 0:
            print(f"switch PWM/DC mode {self._index} on '{self._device}' to 1(PWM)")
            modefile.write_text("1")

    @property
    def enabled(self):
        try:
            return try_read_int(self._manual_auto_file, 1) == 1
        except:
            print(
                f"failed detect fan pwm {self._index} enabled or not on '{self._device}'"
            )
            return False

    def disable(self):
        self._set_enable("0")

    def enable(self):
        self._set_enable("1")

    def _set_enable(self, enable_str: str):
        curr_str = try_read_txt(self._manual_auto_file, "")
        if curr_str != enable_str:
            print(
                f"switch pwm enable {self._index} on {self._device} from {curr_str} to {enable_str}"
            )
            self._manual_auto_file.write_text(enable_str)

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return f"{self._device}_{self._index}"

    @property
    def speed(self):
        return try_read_int(self._speedfile, -1)

    @property
    def pwm(self):
        return try_read_int(self._pwmfile, -1)

    def control(self, pwm: int):
        pwm = math.floor(pwm)
        if pwm < 0:
            print(f"warning: setting {self.name} to {pwm}, capping to 0")
            pwm = 0
        if pwm > PWM_MAX:
            print(
                f"warning: setting {self.name} to {pwm}, capping to PWM_MAX ({PWM_MAX})"
            )
            pwm = PWM_MAX

        if not self.enabled:
            self.enable()
        try:
            self._pwmfile.write_text(str(pwm))
            # print(f"setting {self.name} to {pwm}")
        except Exception as e:
            print(f"error: failed write pwm value {pwm} to {self._pwmfile}: {e}")

        self._control = try_read_int(self._pwmfile, -1)
        if self._control != pwm:
            print(f"warn: {self.name} set pwm to {pwm} but read back {self._control}")


type FanList = list[Fan]
