from fancontrol.curve.base import Point
from fancontrol.curve.z_line import Polyline, StraightLine
from fancontrol.tools.functions import Remember, average, maximum
from fancontrol.tools.hwmon import Controller
from fancontrol.tools.constants import PWM_MAX, PWM_MIN

cpu_curve = StraightLine()
cpu_curve.next(Point(temperature=30, pwm=50))
cpu_curve.next(Point(temperature=50, pwm=200))
cpu_curve.next(Point(temperature=50, pwm=PWM_MAX))

wall_curve = StraightLine()
wall_curve.next(Point(temperature=30, pwm=50))
wall_curve.next(Point(temperature=45, pwm=PWM_MAX))

back_curve2 = StraightLine()
back_curve2.next(Point(temperature=3, pwm=PWM_MIN))
back_curve2.next(Point(temperature=3, pwm=100))
back_curve2.next(Point(temperature=5, pwm=PWM_MAX))

pci_curve = StraightLine()
pci_curve.next(Point(temperature=30, pwm=120))
pci_curve.next(Point(temperature=45, pwm=PWM_MAX))


pci_curve = Polyline()
pci_curve.next(Point(temperature=49, pwm=120))
pci_curve.next(Point(temperature=50, pwm=140))
pci_curve.next(Point(temperature=51, pwm=160))
pci_curve.next(Point(temperature=52, pwm=180))
pci_curve.next(Point(temperature=53, pwm=200))
pci_curve.next(Point(temperature=54, pwm=PWM_MAX))


FAN_CPU = 2
FAN_BACK = 3
FAN_PCI = 4
FAN_WALL = 6

cpu_rem = Remember()
whole_rem = Remember()
pci_rem = Remember()


def control(
    k10temp: Controller,
    nvme: Controller,
    nouveau: Controller,
    nct6795: Controller,
    SATA: Controller,
):
    cpu_temp = average(k10temp.maximum(), nct6795.find("CPUTIN"))
    cpu_rem.add(cpu_temp)
    print(f"cpu: {(cpu_temp)}")

    pci_temp = average(
        nouveau.maximum(),
        nct6795.find("SYSTIN"),
        nvme.average(),
    )
    pci_rem.add(pci_temp)
    print(f"pci: {(pci_temp)}")

    system_temp = average(
        maximum(nct6795.search(r"AUXTIN")),
        pci_temp,
    )
    print(f"system: {(system_temp)}")

    disks_temp = SATA.maximum()
    print(f"disks: {(disks_temp)}")

    whole_system = maximum(disks_temp, system_temp)
    whole_rem.add(whole_system)

    incre_max = maximum(cpu_rem.increasing(), whole_rem.increasing(), 0)
    print(f"increasing: {(incre_max)}")
    total_max = maximum(
        cpu_rem.weightedAverage(),
        nvme.maximum(),
        nct6795.find("SYSTIN"),
        disks_temp,
    )

    nct6795.control(FAN_CPU, cpu_curve.convert(cpu_temp))
    nct6795.control(FAN_WALL, wall_curve.convert(whole_system))

    if total_max and total_max > 50:
        print(f"something is hot! ({total_max})")
        nct6795.control(FAN_BACK, back_curve1.convert(incre_max))
    else:
        nct6795.control(FAN_BACK, back_curve2.convert(incre_max))

    nct6795.control(FAN_PCI, pci_curve.convert(pci_rem.weightedAverage()))


if __name__ == "__main__":
    import fancontrol.main
    fancontrol.main.start_service(control)
