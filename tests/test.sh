cd /sys/class/hwmon/hwmon3/

# for i in temp*_label; do
# 	echo "$i=$(<$i)"
# done

# for i in pwm3_enable pwm6_enable; do
# 	echo 1 >$i
# done
# for i in pwm3 pwm6; do
# 	echo 40 >$i
# done

for i in pwm?; do
	echo "$i"
	echo 1 >"${i}_enable"

	echo 255 >$i
	read
	echo 50 >$i

	read
	echo 5 >"${i}_enable"
done
