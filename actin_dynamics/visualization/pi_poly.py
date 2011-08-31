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

import bisect
import csv

import numpy

from actin_dynamics.io import data
from actin_dynamics.numerical.interpolation import linear_project

from . import collate

def asymptotic_adppi_v_pi(db_session, ids,
        filename='results/asymptotic_adppi_v_pi.dat'):
    collate.collate_asymptotic_adppi(db_session, ids, filename)

def rho_v_pi(db_session, ids, filename='results/rho_v_pi.dat'):
    results = collate.collate_asymptotic_adppi(db_session, ids, filename)
    half_conc_results = _half_concentrations(results)

    _small_writer(filename, half_conc_results,
            x_name='asymptotic adppi half-concentration (of initial Pi)',
            y_name='release cooperativity')

def halftime_v_rho(db_session, ids, filename='results/halftime_v_rho.dat'):
    collate.basic_collate(db_session, ids, filename,
            x_name='initial_pi_concentration')


def _small_writer(filename, results, x_name, y_name):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(results)


def _half_concentrations(base_results, value=0.5):
    column_ids, rows = base_results
    print 'cids', column_ids
    cols = numpy.transpose(rows)
    concentrations, fractions = cols[0], cols[1:]

    half_concentrations = []
    for cid, fracs in zip(column_ids, fractions):
        # Find surrounding indices -> interpolate (log-linear)
        i = bisect.bisect_left(fracs, value)
        if i >= len(fracs):
            continue
        log_hc = linear_project(numpy.log(fracs[i]), numpy.log(concentrations[i]),
                numpy.log(fracs[i+1]), numpy.log(concentrations[i+1]),
                numpy.log(value))
        hc = numpy.exp(log_hc)
        half_concentrations.append((hc, cid))

    return half_concentrations
