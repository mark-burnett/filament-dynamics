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
import bisect

import numpy

from actin_dynamics.io import data
from actin_dynamics import database

from actin_dynamics.numerical import measurements

def save_timecourse(session_id, experiment_index=0, run_index=0,
        timecourse_filename='results/copoly_timecourse.dat'):
    dbs = database.DBSession()

    session = dbs.query(database.Session).get(session_id)
    run = session.experiments[experiment_index].runs[run_index]

    ftc = run.all_parameters['filament_tip_concentration']
    seed_concentration = run.all_parameters['seed_concentration']
    
    length_data = run.analyses['length']
    # convert to  [factin]
    factin_data = measurements.add_number(measurements.scale(length_data, ftc),
            -seed_concentration)

    pi_data = run.analyses['Pi']

    # File output columns are "time [factin] (error) [pi] (error)"
    combined_data = _combine_timecourse_data(factin_data, pi_data)

    _write_results(timecourse_filename, combined_data,
            'Time (s)', 'Concentration (uM)', 'Data',
            ['[F-actin]', '[F-actin] error', '[Pi]', '[Pi] error'])


def save_halftimes(adp_session_ids, nh_session_ids,
        adp_vectorial_session_id, nh_vectorial_session_id,
        adp_halftime_filename='results/adp_copoly_halftimes.dat',
        nh_halftime_filename='results/nh_copoly_halftimes.dat',
        adp_vectorial_filename='results/adp_copoly_halftimes_vectorial.dat',
        nh_vectorial_filename='results/nh_copoly_halftimes_vectorial.dat'):

    _save_halftimes(adp_session_ids, fraction_name='fraction_adp',
            output_filename=adp_halftime_filename)
    _save_halftimes(nh_session_ids, fraction_name='fraction_nh_atp',
            output_filename=nh_halftime_filename)

    _save_vectorial(adp_vectorial_session_id, fraction_name='fraction_adp',
            output_filename=adp_vectorial_filename)
    _save_vectorial(nh_vectorial_session_id, fraction_name='fraction_nh_atp',
            output_filename=nh_vectorial_filename)

def _save_vectorial(session_id, halftime_name='halftime', fraction_name=None,
        output_filename=None):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    fractions, halftimes = _get_halftimes(session, halftime_name=halftime_name,
            fraction_name=fraction_name)

    rows = zip(fractions, halftimes)

    _small_writer(output_filename, rows, [fraction_name, 'pi halftime'])

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


def _save_halftimes(session_ids, fraction_name=None, output_filename=None):
    dbs = database.DBSession()

    fractions = None
    cooperativities = []
    halftimes = []
    for session_id in session_ids:
        session = dbs.query(database.Session).get(session_id)
        fractions, session_halftimes = _get_halftimes(session,
                fraction_name=fraction_name)

        cooperativities.append(session.parameters['release_cooperativity'])
        halftimes.append(session_halftimes)

    cooperativities, halftimes = zip(*sorted(zip(cooperativities, halftimes)))

    rows = zip(*([fractions] + list(halftimes)))

    _write_results(output_filename, rows,
            fraction_name, 'Halftime', 'Release Cooperativity',
            cooperativities)


def _get_halftimes(session, fraction_name=None, halftime_name='halftime'):
    experiment = session.experiments[0]
    fractions = []
    halftimes = []
    for run in experiment.runs:
        fractions.append(run.parameters[fraction_name])
        halftimes.append(run.get_objective(halftime_name))

    fractions, halftimes = zip(*sorted(zip(fractions, halftimes)))
    return fractions, halftimes


def _combine_timecourse_data(*timecourses):
    results = []
    for times, values, errors in timecourses:
        results.append(values)
        results.append(errors)

    return zip(times, *results)


def _create_rows(parameters, values):
    return numpy.insert(values, 0, parameters, axis=1)

def _write_results(filename, rows, x_name, y_name, column_name, column_ids):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        f.write('# columns: %s\n' % column_name)
        f.write('#     %s\n\n' % str(column_ids))
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(rows)
