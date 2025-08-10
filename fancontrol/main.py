from os import environ
import subprocess
import sys
from pathlib import Path
from time import sleep
from traceback import print_exc

from .control import my_control
from .tools.hwmon import calculate, enter_critical, read_hwmon


def cli():
    controllers = read_hwmon()
    for device_name, controller in controllers.items():
        print("\x1b[48;5;10m  %s  \x1b[0m" % device_name)
        for fan in controller.fans:
            c = "10" if fan.enabled else "11"
            print(
                f"  * \x1b[48;5;{c}mFan {fan.index}\x1b[0m: {fan.speed} RPM / {(fan.pwm/255):.2%}"
            )
        for temp in controller.temperatures:
            print(f"  * Temp {temp.index}: {temp.name}: {temp.degree} °C")


def daemon():
    enter_critical()
    sleep(1)

    controllers = read_hwmon()
    for controller in controllers.values():
        for fan in controller.fans:
            fan.initialize()

    if environ.get("NOTIFY_SOCKET", None):
        print("notify systemd ready")
        subprocess.run(
            ["systemd-notify", "--ready"],
            check=True,
            stderr=subprocess.STDOUT,
            stdout=sys.stderr,
            stdin=subprocess.DEVNULL,
        )
    else:
        print("skip systemd, no enviroment")
        
    try:
        while True:
            calculate(my_control)
            sleep(5)
    except KeyboardInterrupt:
        print("\nbye~")
    except:
        print_exc()

    enter_critical()


if __name__ == "__main__":
    cli()
