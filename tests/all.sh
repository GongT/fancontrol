cd /sys/class/hwmon/hwmon4/

LVL=$1

for i in pwm?; do
	echo "$i"
	echo 1 >"${i}_enable"
	echo "$LVL" >"${i}"
done
