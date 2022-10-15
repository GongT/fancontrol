#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
source lib.sh

mapfile -t LINES < <(ncat --recv-only 127.0.0.1 7634 | sed 's#||#\n#g')

IS_HIGH=
for LINE in "${LINES[@]}"; do
	if [[ $LINE == '|'* ]]; then
		LINE=${LINE:1}
	fi
	mapfile -t -d '|' PARTS < <(echo "$LINE")

	PATH="${PARTS[0]}"
	NAME="${PARTS[1]}"
	VAL="${PARTS[2]}"
	TYPE="${PARTS[3]}"
	# echo "$PATH - $NAME - $VAL - $TYPE"

	if [[ $NAME == "ST1000DM003-1ER162" ]]; then
		continue
	fi

	if [[ $VAL -gt 40 ]]; then
		IS_HIGH=yes
		echo "temperature of $PATH($NAME) is high - $VAL$TYPE" >&2
	fi
done

detect_controller
if [[ $IS_HIGH == yes ]]; then
	echo "disk is hot, set fan speed to 210"
	fan_level 6 210
else
	echo "no disk hot, set fan speed to 60"
	fan_level 6 60
fi
