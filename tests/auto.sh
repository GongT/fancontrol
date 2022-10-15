#!/usr/bin/env bash

set -Eeuo pipefail

cd /sys/class/hwmon/hwmon3/
echo "set pwm {$1} to auto"
echo 5 >"pwm${1}_enable"
