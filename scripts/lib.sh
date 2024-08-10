#!/usr/bin/env bash

export PATH=/bin:/usr/bin:/usr/local/bin:/usr/sbin
HWM_DIR=

function detect_controller() {
	for I in /sys/class/hwmon/*/name; do
		NAME=$(cat "$I" || true)
		if [[ $NAME == "nct6795" ]]; then
			HWM_DIR="$(dirname "$I")"
		fi
	done

	if ! [[ $HWM_DIR ]]; then
		echo "PWM controller not found" >&2
		exit 1
	fi
}

function fan_level() {
	local NUM=$1 VALUE=$2
	echo " * pwm${NUM} --> $2" >&2
	echo 1 >"$HWM_DIR/pwm${NUM}_enable"
	echo "$VALUE" >"$HWM_DIR/pwm${NUM}"
}

function get_fan_level() {
	local NUM=$1
	cat "$HWM_DIR/pwm${NUM}"
}
