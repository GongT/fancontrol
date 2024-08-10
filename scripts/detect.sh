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

	DEVNAME="${PARTS[0]}"
	NAME="${PARTS[1]}"
	VAL="${PARTS[2]}"
	TYPE="${PARTS[3]}"
	# echo "$DEVNAME - $NAME - $VAL - $TYPE"

	if [[ $NAME == "ST1000DM003-1ER162" ]] || [[ $VAL == "ERR" ]]; then
		continue
	fi

	if [[ 45 -le $VAL ]]; then
		IS_HIGH=yes
		echo "temperature of $DEVNAME($NAME) is high - $VAL$TYPE" >&2
	fi
done

declare -i CURRENT MAX=210 MIN=60 FAN_INDEX=6
detect_controller

CURRENT=$(get_fan_level $FAN_INDEX)
if [[ $CURRENT -lt $MIN ]]; then
	CURRENT=$MIN
fi
if [[ $CURRENT -gt $MAX ]]; then
	CURRENT=$MAX
fi

if [[ $IS_HIGH == yes ]]; then
	CURRENT=$((CURRENT + 10))
	if [[ $CURRENT -gt $MAX ]]; then
		CURRENT=$MAX
	fi
	echo "disk is hot, set fan speed to $CURRENT"
else
	echo "no disk hot, set fan speed to $MIN"
	CURRENT=$MIN
fi
fan_level $FAN_INDEX "$CURRENT"
