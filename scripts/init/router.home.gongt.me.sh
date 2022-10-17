#!/usr/bin/env bash

for i in 1 2 3 4 5 6; do
	echo "set fan speed $i to high"
	fan_level "$i" 255
done
