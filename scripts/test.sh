while true; do
	printf '\x1bc'
	printf "value             %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4)
	printf "enable            %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_enable)
	printf "floor             %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_floor)
	printf "mode              %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_mode)
	printf "start             %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_start)
	printf "step_down_time    %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_step_down_time)
	printf "step_up_time      %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_step_up_time)
	printf "stop_time         %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_stop_time)
	printf "target_temp       %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_target_temp)
	printf "temp_sel          %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_temp_sel)
	printf "temp_tolerance    %s\n" $(</sys/devices/platform/nct6775.2592/hwmon/hwmon1/pwm4_temp_tolerance)
	sleep 0.1
done
