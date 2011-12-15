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

from actin_dynamics import database
from actin_dynamics.io import data

def save(session_ids, output_filename='results/melki_rate_sensitivities.dat'):
    dbs = database.DBSession()
    rows = []
    for session_id in session_ids:
        session = dbs.query(database.Session).get(session_id)
        cooperativity = session.parameters['release_cooperativity']
        rate, halftime, halftime_error, low_sens, high_sens, sensitivity = calculate(session)

        halftime_fit_error = abs(halftime - 388)
        total_halftime_error = halftime_error + halftime_fit_error

        total_rate_error = total_halftime_error / sensitivity

        rows.append([cooperativity, rate, total_rate_error,
            halftime, halftime_error, low_sens, high_sens, sensitivity])

    _small_writer(output_filename, sorted(rows),
            ['release_cooperativity', 'release_rate', 'release rate error',
                'halftime', 'halftime error',
                'low sens', 'high sens', 'average sensitivity'])



def calculate(session, parameter_name='release_rate',
        objective_name='halftime', error_name='halftime_error'):
    runs = session.experiments[0].runs

    us_parameters = [r.parameters[parameter_name] for r in runs]
    us_objectives = [r.get_objective(objective_name) for r in runs]
    us_errors = [r.get_objective(error_name) for r in runs]

    parameters, objectives, errors = zip(*sorted(
        zip(us_parameters, us_objectives, us_errors)))

    base_par = parameters[1]
    base_obj = objectives[1]
    base_error = errors[1]

    low_par = (parameters[0] - base_par)
    high_par = (parameters[2] - base_par)

    low_obj = (objectives[0] - base_obj)
    high_obj = (objectives[2] - base_obj)

    low_sense = abs(low_obj / low_par)
    high_sense = abs(high_obj / high_par)

    return (base_par, base_obj, base_error, low_sense, high_sense,
        (low_sense + high_sense) / 2)


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
