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
import scipy.stats

from actin_dynamics import database
from actin_dynamics.io import data


def get_lagtimes(session):
    results = []
    for run in session.experiments[0].runs:
        fnc = run.parameters['filament_tip_concentration']
        f_ht = run.get_objective('f_halftime')
        p_ht = run.get_objective('p_halftime')
        if f_ht is not None and p_ht is not None:
            results.append((fnc, p_ht - f_ht))

    results.sort()
    fncs, lagtimes = zip(*results)
    cooperativity = session.parameters.get('release_cooperativity', None)
    return cooperativity, fncs, lagtimes

def scale_lagtimes(lagtimes):
    return numpy.array(lagtimes) / lagtimes[-1]

def save_lagtimes(session_ids,
        cooperative_output_filename='results/fnc_cooperative_lagtimes.dat',
        vectorial_output_filename='results/fnc_vectorial_lagtimes.dat'):
    dbs = database.DBSession()

    fncs = None
    vectorial_lagtimes = None
    all_lagtimes = []
    for sid in session_ids:
        session = dbs.query(database.Session).get(sid)
        cooperativity, fncs, lagtimes = get_lagtimes(session)
        s_lagtimes = scale_lagtimes(lagtimes)
        if cooperativity is not None:
            all_lagtimes.append((cooperativity, s_lagtimes))
        else:
            vectorial_lagtimes = s_lagtimes

    if all_lagtimes:
        all_lagtimes.sort()
        cooperativities, cooperative_lagtimes = zip(*all_lagtimes)
#        cooperative_lagtimes = numpy.array(cooperative_lagtimes)

        rhos = ['%.0e' % c for c in cooperativities]
        rows = zip(fncs, *cooperative_lagtimes)

        _write_results(cooperative_output_filename, rows,
                'FNC', 'Lagtime', 'Release Cooperativity',
                rhos)

    if vectorial_lagtimes is not None:
        _small_writer(vectorial_output_filename,
                zip(fncs, vectorial_lagtimes),
                ['fnc', 'lagtime'],
                header='# Lagtime for vectorial model.\n')

def _get_single_lagtime(session):
    cooperativity = session.parameters.get('release_cooperativity', None)

    runs = session.experiments[0].runs
    lagtimes = []
    for r in runs:
        p_ht = r.get_objective('p_halftime')
        f_ht = r.get_objective('f_halftime')
        if p_ht is not None and f_ht is not None:
            lagtimes.append(p_ht - f_ht)

    lagtime = numpy.mean(lagtimes)
    error = numpy.std(lagtimes, ddof=1)

    return cooperativity, lagtime, error, len(lagtimes)


def save_qof(numerator_session_ids, denominator_session_ids, alpha=0.01,
        cooperative_output_filename='results/fnc_cooperative_qof.dat',
        vectorial_output_filename='results/fnc_vectorial_qof.dat'):
    TARGET = 620.69 / 166.7 # about 3.72
    dbs = database.DBSession()


    n_rows = []
    for nsid in numerator_session_ids:
        session = dbs.query(database.Session).get(nsid)
        n_rows.append(_get_single_lagtime(session))

    d_rows = []
    for dsid in denominator_session_ids:
        session = dbs.query(database.Session).get(dsid)
        d_rows.append(_get_single_lagtime(session))


    n_rows.sort()
    d_rows.sort()

    coop_results = []
    vec_results = None
    for nrow, drow in zip(n_rows, d_rows):
        nrho, nval, nerr, nnum = nrow
        drho, dval, derr, dnum = drow
        if nrho != drho:
            raise RuntimeError("Numerator and Denominator FNCs don't match.")
#        if nnum != dnum:
#            raise RuntimeError("Numerator and Denominator simulation counts don't match.")

        qof = (nval / dval - TARGET)**2

        fit_std_error = numpy.sqrt((nerr/dval)**2 + (nval * derr / dval**2)**2)
        t = scipy.stats.t.ppf(1 - alpha/2, min(nnum, dnum) - 1)
        ci_size = t * fit_std_error

        if nrho is not None:
            coop_results.append((nrho, qof, qof - ci_size, qof + ci_size,
                ci_size/qof * 100))
        else:
            vec_results = (qof, qof - ci_size, qof + ci_size, ci_size/qof * 100)

    if coop_results:
        coop_results.sort()
        _small_writer(cooperative_output_filename, coop_results,
                ['Cooperativity', 'Chi^2', 'Min CI', 'Max CI', '% Error'],
                header="# Cooperative quality of fit for Carlier 86\n")

    if vec_results:
        _small_writer(vectorial_output_filename, [vec_results],
                ['Chi^2', 'Min CI', 'Max CI', '% Error'],
                header="# Vectorial quality of fit for Carlier 86\n")



# Old stuff (maybe not that useful)
def all(cooperative_session_ids, vectorial_session_id):
    multiple(cooperative_session_ids, objective_name='halftime',
            output_filename='results/fnc_pi_halftimes_cooperative.dat')
    single(vectorial_session_id, objective_name='halftime',
            output_filename='results/fnc_pi_halftimes_vectorial.dat')

    multiple(cooperative_session_ids, objective_name='factin_halftime',
            output_filename='results/fnc_f_halftimes_cooperative.dat')
    single(vectorial_session_id, objective_name='factin_halftime',
            output_filename='results/fnc_f_halftimes_vectorial.dat')

#    multiple(cooperative_session_ids, objective_name='adppi_peak_time',
#            output_filename='results/fnc_adppi_peak_times_cooperative.dat')
#    single(vectorial_session_id, objective_name='adppi_peak_time',
#            output_filename='results/fnc_adppi_peak_times_vectorial.dat')
#
#    multiple(cooperative_session_ids, objective_name='adppi_peak_value',
#            output_filename='results/fnc_adppi_peak_values_cooperative.dat')
#    single(vectorial_session_id, objective_name='adppi_peak_value',
#            output_filename='results/fnc_adppi_peak_values_vectorial.dat')

def vectorial(session_id):
    single(session_id, output_filename='results/fnc_halftimes_vectorial.dat')

def single(session_id, objective_name='halftime',
        output_filename='results/fnc_halftimes.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    results = _get_objective_v_concentration(session,
            concentration_name='filament_tip_concentration',
            objective_name=objective_name)

    _small_writer(output_filename, results, ['fnc', 'halftime'])

def multiple(session_ids, objective_name='halftime',
        output_filename='results/fnc_halftimes_cooperative.dat'):
    dbs = database.DBSession()
    cooperativities = []
    results = []
    fncs = None
    for sid in session_ids:
        session = dbs.query(database.Session).get(sid)

        cooperativities.append(session.experiments[0]
                .all_parameters['release_cooperativity'])
        fnc_plus_results = _get_objective_v_concentration(session,
            concentration_name='filament_tip_concentration',
            objective_name=objective_name)
        fncs, c_results = zip(*fnc_plus_results)
        results.append(c_results)
    results = numpy.array(results).transpose()
    rows = _create_rows(fncs, results)

    _write_results(output_filename, rows,
            'FNC', objective_name, 'Release Cooperativity',
            cooperativities)


def _get_objective_v_concentration(session, concentration_name, objective_name='halftime'):
    e = session.experiments[0]
    concentrations = []
    values = []
    for run in e.runs:
        c = run.parameters[concentration_name]
        v = run.get_objective(objective_name)
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
