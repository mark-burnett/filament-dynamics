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

from actin_dynamics import database
from actin_dynamics.io import data

def vectorial(session_id):
    single(session_id, output_filename='results/vectorial_fnc_halftimes.dat')

def single(session_id, output_filename='results/single_fnc_halftimes.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    results = _get_single_halftimes(session,
            concentration_name='filament_tip_concentration')

    _small_writer(output_filename, results, ['fnc', 'halftime'])

def multiple(session_ids, output_filename='results/fnc_halftimes.dat'):
    dbs = database.DBSession()
    cooperativities = []
    results = []
    fncs = None
    for sid in session_ids:
        session = dbs.query(database.Session).get(sid)

        cooperativities.append(session.experiments[0]
                .all_parameters['release_cooperativity'])
        fnc_plus_results = _get_single_halftimes(session,
            concentration_name='filament_tip_concentration')
        fncs, c_results = zip(*fnc_plus_results)
        results.append(c_results)
    results = numpy.array(results).transpose()
    rows = _create_rows(fncs, results)

    _write_results(output_filename, rows,
            'FNC', 'Halftime', 'Release Cooperativity',
            cooperativities)


def _get_single_halftimes(session, concentration_name):
    e = session.experiments[0]
    concentrations = []
    values = []
    for run in e.runs:
        c = run.parameters[concentration_name]
        v = run.objectives[0].value
        concentrations.append(c)
        values.append(v)
    return sorted(zip(concentrations, values))

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


def save_halftimes(session_id, halftime_filename='results/fnc_halftimes.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    fnc_mesh, cooperativities, halftime_results = _get_halftimes(
            session, concentration_name='filament_tip_concentration')

    _write_results(halftime_filename,
            _create_rows(fnc_mesh, halftime_results),
            'FNC', 'Halftime', 'Release Cooperativity',
            cooperativities)

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
