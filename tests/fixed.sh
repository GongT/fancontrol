#!/usr/bin/env bash

set -Eeuo pipefail

DEV=$1
VALUE=$2

cd /sys/class/hwmon/hwmon4/
echo "set pwm {$DEV} to fixed ($VALUE)"
echo 1 >"pwm${DEV}_enable"
echo "$VALUE" >"pwm${DEV}"
