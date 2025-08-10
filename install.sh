#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

rm -rf dist
python -m venv /usr/local/libexec/fanspeed --upgrade

poetry build -f wheel
/usr/local/libexec/fanspeed/bin/pip install dist/*.whl
/usr/local/libexec/fanspeed/bin/pip install --upgrade --force-reinstall --no-deps dist/*.whl
rm -f /usr/local/bin/fanctl
ln -s /usr/local/libexec/fanspeed/bin/fanctl /usr/local/bin/fanctl

mkdir -p /usr/local/lib/systemd/system /etc/fanspeed
cp services/fanspeed.service /usr/local/lib/systemd/system/fanspeed.service
cp services/fanspeed-fullspeed.service /usr/local/lib/systemd/system/fanspeed-fullspeed.service


echo ""

systemctl daemon-reload
systemctl reenable fanspeed.service
systemctl reset-failed fanspeed
systemctl restart fanspeed.service --no-block
