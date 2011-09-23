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

from actin_dynamics import database
from actin_dynamics.numerical import measurements

from . import collate

def timecourse(db_session, session_id, experiment_index=0, run_index=0,
        filename='results/short_time.dat'):
    session = db_session.query(database.Session).get(session_id)
    run = session.experiments[experiment_index].runs[run_index]

    ftc = run.all_parameters['filament_tip_concentration']
    seed_concentration = run.all_parameters['seed_concentration']

    length_data = run.analyses['length']
    # convert to  [factin]
#    factin_data = measurements.scale(length_data, ftc)
    factin_data = measurements.add_number(measurements.scale(length_data, ftc),
            -seed_concentration)

#    pi_random_data = run.analyses['Pi_random']
#    pi_vectorial_data = run.analyses['Pi_vectorial']
    pi_data = run.analyses['Pi']

    combined_data = _combine_timecourse_data(factin_data,
#            pi_random_data, pi_vectorial_data,
            pi_data)

    _write_results(filename, combined_data,
            'Time (s)', 'Concentration (uM)', 'Data',
            ['[F-actin]',
#                '[Pi_random]', '[Pi_vectorial]',
                '[Pi_other]'])


def _combine_timecourse_data(*timecourses):
    results = []
    for times, values, errors in timecourses:
        results.append(values)
        results.append(errors)

    return zip(times, *results)


def _write_results(filename, rows, x_name, y_name, column_name, column_ids):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        f.write('# columns: %s\n' % column_name)
        f.write('#     %s\n\n' % column_ids)
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(rows)
