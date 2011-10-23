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
import numpy

from actin_dynamics import database
from actin_dynamics.io import data


def save(session_id,
        output_filename='results/depolymerization_timecourses.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    times = None
    values = []
    for run in session.experiments[0].runs:
        times, run_values = _get_timecourse(run)
        values.append(run_values)

    tv = numpy.transpose(values)
    results = numpy.vstack((times, values))
    results = numpy.transpose(results)

#    results = list(times)
#    results.extend(list(values))
#    results = numpy.array(results)
#    results = numpy.transpose(results)

    _small_writer(output_filename, results, ['times', 'filament_length'])

def _get_timecourse(run):
    # Grab the analysis
    times, values, errors = run.analyses['length']
    times = numpy.array(times)

    values = numpy.array(values)
    numpy.putmask(values, values < 50, float('nan'))

    polymerization_duration = run.all_parameters['polymerization_duration']

    return times, values

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
