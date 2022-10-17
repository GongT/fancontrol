#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
source lib.sh

while ! detect_controller; do
	sleep 5
done

F="init/$(hostname).sh"
echo "load: ${F}"
source "$F"
