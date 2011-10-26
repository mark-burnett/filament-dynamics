#!/usr/bin/env python
#    Copyright (C) 2010 Mark Burnett
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

FRACTIONAL_DX = 0.001

FILENAME_TEMPLATE = 'definitions/sensitivity/rho_%s.yaml'

FILE_TEMPLATE = \
"""
name: 'Halftime Sensitivity, rho_c = %s'

import:
    - 'sensitivity/base.yaml'
    - 'random_cooperative_model.yaml'

global_parameters:
    release_cooperativity: %s

parameter_specifications:
    halftime_sensitivity:
        simulation:
            release_rate:
                lower_bound: %s
                upper_bound: %s
                mesh_type:   linear
                num_points:  3
"""

from actin_dynamics.io import data

def main():
    rate_results = data.load_data('results/melki_rates.dat')

    cooperativities, rates = rate_results[0], rate_results[1]

    for rho, r in zip(cooperativities, rates):
        lower_rate = r * (1 - FRACTIONAL_DX)
        upper_rate = r * (1 + FRACTIONAL_DX)
        with open(FILENAME_TEMPLATE % rho, 'w') as f:
            f.write(FILE_TEMPLATE % (rho, rho, lower_rate, upper_rate))

if '__main__' == __name__:
    main()
