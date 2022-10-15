cd /sys/class/hwmon/hwmon3/

LVL=200

for i in 1 2 3 4 5; do
	echo "pwm$i"
	echo 1 >"pwm${i}_enable"
	echo "$LVL" >"pwm${i}"
done

for i in 6; do
	echo "pwm$i"
	echo 1 >"pwm${i}_enable"
	echo "50" >"pwm${i}"
done
