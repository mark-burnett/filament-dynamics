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

import csv

import sqlalchemy
import numpy

from actin_dynamics import database
from actin_dynamics.io import data


def save_timecourses(session_id,
        output_filename='results/carlier_86_timecourses.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    run = session.experiments[0].runs[0]

    times, atp_vals, atp_errors = run.analyses['F_ATP']
    times, adppi_vals, adppi_errors = run.analyses['F_ADPPi']
    times, adp_vals, adp_errors = run.analyses['F_ADP']

    times, pi_vals, pi_errors = run.analyses['Pi']

    times, length_vals, length_errors = run.analyses['length']

    rows = zip(times, length_vals,
            atp_vals, adppi_vals, adp_vals, pi_vals)

    _small_writer(output_filename, rows,
            ['Time (s)', 'length',
                'F-ATP-actin', 'F-ADPPi-actin', 'F-ADP-actin',
                '[Pi] uM'])


def _small_writer(filename, results, names, header=None):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        if header:
            f.write(header)
        for i, name in enumerate(names):
            f.write('# Column %i: %s\n' % ((i + 1), name))
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(results)
