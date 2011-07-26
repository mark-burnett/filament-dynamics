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


def pi_poly(db_session, ids, filename='pi_poly_asymptotic_adppi.dat',
        half_conc_filename='pi_poly_half_concentration.dat'):
    results = collate.collate_asymptotic_adppi(db_session, ids, filename)
    half_conc_results = _half_concentrations(results)

    _small_writer(half_conc_filename, half_conc_results,
            x_name='asymptotic adppi half-concentration (of initial Pi)',
            y_name='release cooperativity')


def pi_poly_tagged(db_session, ids, filename='pi_poly_tagged_pi_halftime.dat',
        doubling_conc_filename='pi_poly_tagged_doubling_conc.dat',
        random_halftime=390):
    results = collate.basic_collate(db_session, ids, filename,
            x_name='initial_pi_concentration')

    dc_results = _doubling_concentrations(results, random_halftime)
    _small_writer(doubling_conc_filename, dc_results,
            x_name='doubling concentration',
            y_name='release cooperativity')


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
    cols = numpy.transpose(rows)

    half_concentrations = []
    for col in cols:
        # Find surrounding indices -> interpolate (log-linear)
        i = bisect.bisect_left(col, value)
        log_hc = linear_project(numpy.log(column_ids[i]), col[i],
                numpy.log(column_ids[i+1]), col[i+1],
                value)
        hc = numpy.exp(log_hc)
        half_concentrations.append(hc)

    return zip(half_concentrations, column_ids)


def _doubling_concentrations(base_results, random_halftime):
    '''
    Calculates the concentration required to double the halftime
    (compared with zero concentration/random model)
    '''
    column_ids, rows = base_results
    cols = numpy.transpose(rows)

    doubling_concentrations = []
    for col in cols:
        # Find surrounding indices -> interpolate (log-log)
        i = bisect.bisect_left(col, 2 * random_halftime)
        log_dc = linear_project(numpy.log(column_ids[i]), numpy.log(col[i]),
                numpy.log(column_ids[i+1]), numpy.log(col[i+1]),
                numpy.log(2 * random_halftime))
        dc = numpy.exp(log_dc)
        doubling_concentrations.append(dc)

    return zip(doubling_concentrations, column_ids)

