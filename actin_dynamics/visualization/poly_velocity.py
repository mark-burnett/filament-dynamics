#    Copyright (C) 2012 Mark Burnett
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

def save_vs_cooperativity(cooperative_session_ids, vectorial_session_id,
        cooperative_filename='results/cc_d_cooperative.dat',
        vectorial_filename='results/cc_d_vectorial.dat'):
    results = sorted(map(get_cc_d, cooperative_session_ids))

    _small_writer(cooperative_filename, results,
            ['Release Cooperativity', 'Critical Concentration (uM)',
                'Diffusion Coefficient (mon/s^2)'])

    junk, vec_cc, vec_D = get_cc_d(vectorial_session_id)
    _small_writer(vectorial_filename, [(vec_cc, vec_D)],
            ['Critical Concentration (uM)',
                'Diffusion Coefficient (mon/s^2)'])


def save_vs_parameter(session_id, output_filename='results/cc_d_tip.dat',
        parameter='barbed_tip_release_rate'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    results = []
    for run in session.experiments[0].runs:
        results.append(get_cc_d_run(run, parameter=parameter))

    results.sort()

    _small_writer(output_filename, results,
            [parameter, 'Critical Concentration (uM)',
                'Diffusion Coefficient (mon/s^2)'])



def get_cc_d(session_id):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    run = session.experiments[0].runs[0]
    cc = run.get_objective('final_ATP_concentration')
    D = run.get_objective('diffusion_coefficient')

    cooperativity = run.all_parameters.get(parameter)

    return cooperativity, cc, D

def get_cc_d_run(run, parameter='release_cooperativity'):
    cc = run.get_objective('final_ATP_concentration')
    D = run.get_objective('diffusion_coefficient')

    cooperativity = run.all_parameters.get(parameter)

    return cooperativity, cc, D

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

