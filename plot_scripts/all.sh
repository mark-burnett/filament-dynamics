#!/usr/bin/env bash

rm plots/*.eps
plot_scripts/melki.py &
plot_scripts/copoly.py &
plot_scripts/pi_poly.py &

wait
