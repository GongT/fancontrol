#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s inherit_errexit extglob nullglob globstar lastpipe shift_verbose

for ROOT in /sys/class/hwmon/*; do
	echo "$(basename $ROOT)"
	for F in $ROOT/*; do
		if [[ -f "$F" ]]; then
			echo "    $(basename "$F") - $(head -n1 "$F" 2>/dev/null)"
		fi
	done
done
