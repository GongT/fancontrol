from fancontrol.curve.base import Point
from fancontrol.curve.z_line import Polyline, StraightLine
from fancontrol.tools.fs import try_read_int, try_read_txt
from fancontrol.tools.functions import Remember, average, maximum
from fancontrol.tools.hddtemp import hddtemp_client
from fancontrol.tools.hwmon import Controller, calculate, enter_critical, read_hwmon

cpu_curve = StraightLine()
cpu_curve.next(Point(temperature=30, pwm=50))
cpu_curve.next(Point(temperature=50, pwm=200))
cpu_curve.next(Point(temperature=50, pwm=255))

wall_curve = StraightLine()
wall_curve.next(Point(temperature=30, pwm=50))
wall_curve.next(Point(temperature=45, pwm=255))

back_curve = StraightLine()
back_curve.next(Point(temperature=3, pwm=0))
back_curve.next(Point(temperature=3, pwm=100))
back_curve.next(Point(temperature=5, pwm=255))

pci_curve = StraightLine()
pci_curve.next(Point(temperature=30, pwm=120))
pci_curve.next(Point(temperature=45, pwm=255))


FAN_CPU = 2
FAN_BACK = 3
FAN_PCI = 4
FAN_WALL = 6

cpu_rem = Remember()
whole_rem = Remember()
pci_rem = Remember()


def my_control(
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

    nct6795.control(FAN_CPU, cpu_curve.convert(cpu_temp))
    nct6795.control(FAN_WALL, wall_curve.convert(whole_system))

    incre_max = maximum(cpu_rem.increasing(), whole_rem.increasing())
    nct6795.control(FAN_BACK, back_curve.convert(incre_max))

    nct6795.control(FAN_PCI, pci_curve.convert(pci_rem.weightedAverage()))
