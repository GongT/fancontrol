# fanspeed control

read and write `/sys/class/hwmon/hwmon*` with python script

# Install

1. load all required drivers. for simplicity, install `lm-sensors` from package repositories and run `sensors-detect`.
1. install python3 and poetry on system
1. run `install.sh`
1. modify `/etc/fanspeed/control.py` to match your need

# Api

virtual env is created at `/usr/local/libexec/fanspeed`

// TODO
