#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
source lib.sh

while ! detect_controller; do
	sleep 5
done

for i in 1 2 3 4 5; do
	echo "set fan speed $i to low"
	fan_level "$i" 120
done
for i in 6; do
	echo "set fan speed $i to high"
	fan_level "$i" 210
done
