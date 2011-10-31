#!/usr/bin/env python
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

COOP_FILENAME_TEMPLATE = 'definitions/fit_rates/rho_%i.yaml'
COOP_FILE_TEMPLATE = \
"""global_parameters:
    release_cooperativity: %s
    release_rate: %s
"""

VEC_FILENAME = 'definitions/sensitivity/vectorial.yaml'
VEC_FILE_TEMPLATE = \
"""global_parameters:
    release_rate: %s
"""

from actin_dynamics.io import data

def main():
    # Cooperative parts
    rate_results = data.load_data('results/melki_rates.dat')

    cooperativities, rates = rate_results[0], rate_results[1]

    for rho, r in zip(cooperativities, rates):
        with open(COOP_FILENAME_TEMPLATE % rho, 'w') as f:
            f.write(COOP_FILE_TEMPLATE % (rho, r))

    # Vectorial part
    vec_rates = data.load_data('results/melki_vectorial_rate.dat')

    r = vec_rates[1][0]

    with open(VEC_FILENAME, 'w') as f:
        f.write(VEC_FILE_TEMPLATE % r)


if '__main__' == __name__:
    main()
