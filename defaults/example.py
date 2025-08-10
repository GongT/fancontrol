from fancontrol.curve.base import Point
from fancontrol.curve.z_line import StraightLine
from fancontrol.tools.constants import PWM_MAX, PWM_MIN
from fancontrol.tools.functions import Remember, average, maximum
from fancontrol.tools.hwmon import Controller

cpu_curve = StraightLine()
cpu_curve.next(Point(temperature=30, pwm=50))
cpu_curve.next(Point(temperature=50, pwm=200))
cpu_curve.next(Point(temperature=50, pwm=PWM_MAX))

FAN_CPU = 1

cpu_rem = Remember()


def control(k10temp: Controller, nct6795: Controller):
    cpu_temp = average(k10temp.maximum())

    nct6795.control(FAN_CPU, cpu_curve.convert(cpu_temp))

if __name__ == "__main__":
    import fancontrol.main
    fancontrol.main.start_service(control)
