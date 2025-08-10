from collections.abc import Callable
import subprocess
import sys
from os import environ
from pathlib import Path
from time import sleep
from traceback import print_exc

from .tools.hwmon import calculate, enter_critical, read_hwmon


def cli():
    controllers = read_hwmon()
    for device_name, controller in controllers.items():
        print("\x1b[48;5;10m  %s  \x1b[0m" % device_name)
        for fan in controller.fans:
            c = "10" if fan.enabled else "11"
            print(
                f"  * \x1b[48;5;{c}mFan {fan.index}\x1b[0m: {fan.speed} RPM / {fan.pwm} | {(fan.pwm/255):.2%}"
            )
        for temp in controller.temperatures:
            v = temp.degree
            if not v:
                continue

            print(f"  * Temp {temp.index}: {temp.name}: {v} °C")


def _load_control(path: Path):
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("fancontrol.control", path.as_posix())
    foo = importlib.util.module_from_spec(spec)
    sys.modules["fancontrol.control"] = foo
    spec.loader.exec_module(foo)
    return foo.control


def _daemon():
    if len(sys.argv) == 1:
        _daemon_boot(Path("/etc/fanspeed/control.py"))
    elif len(sys.argv) == 2:
        action = sys.argv[1]
        if action == "--full":
            enter_critical()
            return

        elif action.endswith(".py"):
            _daemon_boot(Path(action).absolute())
            return

    print("usage: fansd [--full|/path/to/control.py]")
    sys.exit(1)

def _daemon_boot(file: Path):
    if not file.exists():
        print(f"Control file '{file}' does not exist")
        sys.exit(1)

    control_function = _load_control(file)
    if not isinstance(control_function, Callable):
        print(f"'control' function is not defined or callable")
        sys.exit(1)

    start_service(control_function)

def start_service(control_function: Callable):

    controllers = read_hwmon()

    enter_critical()

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
            calculate(control_function)
            sleep(5)
    except KeyboardInterrupt:
        print("\nbye~")
    except:
        print_exc()

    enter_critical()


if __name__ == "__main__":
    cli()
