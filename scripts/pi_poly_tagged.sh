#!/usr/bin/env bash

#    Copyright (C) 2011 Mark Burnett
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

./sim.sh -n 8 -l -s configuration/pi_poly_tagged/pi_poly_rho_r_1.yaml
./sim.sh -n 0 -l -s configuration/pi_poly_tagged/pi_poly_rho_r_10.yaml
./sim.sh -n 0 -l -s configuration/pi_poly_tagged/pi_poly_rho_r_100.yaml
./sim.sh -n 0 -l -s configuration/pi_poly_tagged/pi_poly_rho_r_1000.yaml
./sim.sh -n 0 -l -s configuration/pi_poly_tagged/pi_poly_rho_r_10000.yaml
