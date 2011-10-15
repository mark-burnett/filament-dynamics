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


def save_halftimes(adp_session_id, nh_session_id,
#        cooperativities=[1, 10, 100, 1000, 10000, 100000, 1000000],
        adp_halftime_filename='results/adp_copoly_halftimes.dat',
        nh_halftime_filename='results/nh_copoly_halftimes.dat'):
    dbs = database.DBSession()
    adp_session = dbs.query(database.Session).get(adp_session_id)
    nh_session = dbs.query(database.Session).get(nh_session_id)

    frac_adp_mesh, adp_cooperativities, adp_halftime_results = _get_halftimes(
            adp_session, concentration_name='fraction_adp')
    frac_nh_mesh, nh_cooperativities, nh_halftime_results = _get_halftimes(
            nh_session, concentration_name='fraction_nh_atp')

    _write_results(adp_halftime_filename,
            _create_rows(frac_adp_mesh, adp_halftime_results),
            'ADP Fraction', 'Halftime', 'Release Cooperativity',
            adp_cooperativities)
    _write_results(nh_halftime_filename,
            _create_rows(frac_nh_mesh, nh_halftime_results),
            'NH Fraction', 'Halftime', 'Release Cooperativity',
            nh_cooperativities)


def _combine_timecourse_data(*timecourses):
    results = []
    for times, values, errors in timecourses:
        results.append(values)
        results.append(errors)

    return zip(times, *results)


def _get_halftimes(session, cooperativity_name='release_cooperativity',
        concentration_name=None):
    # extract meshes
    cooperativities = set()
    concentrations = set()
    e = session.experiments[0]
    for run in e.runs:
        cooperativities.add(run.parameters[cooperativity_name])
        concentrations.add(run.parameters[concentration_name])
    cooperativity_mesh = sorted(list(cooperativities))
    concentration_mesh = sorted(list(concentrations))

    results = - numpy.ones((len(concentration_mesh), len(cooperativity_mesh)))

    ob = e.objectives['halftime']
    for o in ob.objectives:
        conc_i = bisect.bisect_left(concentration_mesh,
                o.run.parameters[concentration_name])
        coop_i = bisect.bisect_left(cooperativity_mesh,
                o.run.parameters[cooperativity_name])
        results[conc_i, coop_i] = o.value

    return concentration_mesh, cooperativity_mesh, results

def _create_rows(parameters, values):
#    parameters = numpy.transpose(numpy.array(parameters))
#    values = numpy.transpose(values)
#    print parameters
#    print values
    return numpy.insert(values, 0, parameters, axis=1)

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
