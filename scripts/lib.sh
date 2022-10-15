#!/usr/bin/env bash

DIR=

function detect_controller() {
	for I in /sys/class/hwmon/*/name; do
		NAME=$(cat "$I" || true)
		if [[ $NAME == "nct6795" ]]; then
			DIR="$(dirname "$I")"
		fi
	done

	if ! [[ $DIR ]]; then
		echo "PWM controller not found" >&2
	fi
}

function fan_level() {
	local NUM=$1 VALUE=$2
	echo " * pwm${NUM} --> $2" >&2
	echo 1 >"$DIR/pwm${NUM}_enable"
	echo "$VALUE" >"$DIR/pwm${NUM}"
}
