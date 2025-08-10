#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s inherit_errexit extglob nullglob globstar lastpipe shift_verbose

cd  "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

OUTPUT=''

SHEBANG="#!/usr/local/libexec/fanspeed/bin/python3"
if [[ -e /etc/machine-id ]]; then
	MACHINE_ID=$(</etc/machine-id)
	if [[ -e "../defaults/${MACHINE_ID}.py" ]]; then
		echo "copy machine config to /etc/fanspeed/control.py"
		OUTPUT=$(
			echo "${SHEBANG}"
			cat "../defaults/${MACHINE_ID}.py" 
		)
	fi
fi
if ! [[ -z "${OUTPUT}" ]] && ! [[ -e /etc/fanspeed/control.py ]]; then
	echo "copy example config to /etc/fanspeed/control.py"
	OUTPUT=$(
		echo "${SHEBANG}"
		cat "../defaults/example.py" 
	)
fi

if [[ -z "${OUTPUT}" ]]; then
	echo "no config file fit for this machine."
	exit 1
fi

BEFORE=$(</etc/fanspeed/control.py)

if [[ "${BEFORE}" != "${OUTPUT}" ]]; then
	echo "config file has changed, updating..."
	echo "${OUTPUT}" >/etc/fanspeed/control.py
	systemctl restart fanspeed.service
fi
