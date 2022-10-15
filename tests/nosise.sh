#!/bin/bash

set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
bash fixed.sh 6 "$1"
bash fixed.sh 3 "$1"


