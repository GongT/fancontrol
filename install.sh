#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
ROOT=$(pwd)
cd services

{
	cat hdd-temp.service
	echo "Environment=ROOT=$ROOT"
} >/usr/lib/systemd/system/hdd-temp.service

{
	cat hdd-temp.timer
} >/usr/lib/systemd/system/hdd-temp.timer

{
	cat hdd-init.service
	echo "Environment=ROOT=$ROOT"
} >/usr/lib/systemd/system/hdd-init.service

systemctl daemon-reload
systemctl enable --now hdd-init.service hdd-temp.timer
