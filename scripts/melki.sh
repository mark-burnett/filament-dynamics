#!/usr/bin/env bash

#    Copyright (C) 2012 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

echo 'Fitting...'
for FILE in definitions/melki/fit_rho_*.yaml; do
    echo $FILE
    ./sim.sh -l -n 0 -s $FILE
    sleep 1
#    bin/simple_fit.py -o pi_fit $FILE &
done

./sim.sh -l -n 0 -s definitions/melki/fit_vectorial.yaml
#bin/simple_fit.py -o pi_fit definitions/melki/fit_vectorial.yaml &
wait

# Probably should wait, so I don't kill everything accidentally
# bin/view_log.py -tf --process_type controller --min_level 50
