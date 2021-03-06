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
import operator

import sqlalchemy

import numpy
import scipy

from actin_dynamics import database
from actin_dynamics.io import data


def session_fits(session_id, fit_length=50,
        output_filename='results/check_fit.dat',
        write=True):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    data = []
    for run in runs:
        parameter = run.parameters['release_rate']
        fitness = run.get_objective('pi_fit')
        if fitness is not None:
            data.append((parameter, fitness))

    fit_sorted_data = sorted(data, key=operator.itemgetter(1))
    px, py = zip(*fit_sorted_data[:fit_length])
    coeffs, R, n, svs, rcond = scipy.polyfit(px, py, 2, full=True)

    x, y = zip(*sorted(data))

    peak = float(-coeffs[1] / (2 * coeffs[0]))
    fit = float(R/fit_length)

    if write:
        p = scipy.polyval(coeffs, x)
        header = '# Parabola peak at %s\n# Parabola R^2/n = %s\n'
        rows = zip(x, y, p)
        _small_writer(output_filename, rows, ['release_rate', 'pi_fit', 'parabola'],
                header=header % (peak, fit))

    return session.parameters.get('release_cooperativity'), peak, fit


def extract_fits(session_ids, output_filename='results/fit_rates.dat',
        fit_length=50):
    dbs = database.DBSession()

    rows = []
    for session_id in session_ids:
        rows.append(session_fits(session_id, fit_length=fit_length,
            write=False))

    rows.sort()

    _small_writer(output_filename, rows, ['release_cooperativity',
        'release_rate', 'parabola R2'])


def save_timecourses(session_ids,
        factin_filename='results/melki_factin_timecourses.dat',
        pi_filename='results/melki_pi_timecourses.dat'):
    dbs = database.DBSession()
    sessions = [dbs.query(database.Session).get(sid) for sid in session_ids]
    cooperativities = [s.parameters['release_cooperativity'] for s in sessions]
    cooperativities, sessions = zip(*sorted(zip(cooperativities, sessions)))

    times = None
    factin_values = []
    pi_values = []
    for session in sessions:
        run = session.experiments[0].runs[0]

        times, fvals, ferrors = run.analyses['factin']
        times, pvals, perrors = run.analyses['Pi']

        factin_values.append(fvals)
        pi_values.append(pvals)

    factin_rows = zip(*([times] + factin_values))
    pi_rows = zip(*([times] + pi_values))

    _write_results(factin_filename, factin_rows, 'Time (s)', 'F-actin (uM)',
            'Release Cooperativitiy', cooperativities)

    _write_results(pi_filename, pi_rows, 'Time (s)', '[Pi] (uM)',
            'Release Cooperativitiy', cooperativities)


def save_timecourse(run, analyses=['factin', 'Pi'],
        output_filename='results/timecourses.dat'):
    times = None
    values = []
    for a in analyses:
        times, avals, aerrors = run.analyses[a]
        values.append(avals)

    rows = []
    for i, t in enumerate(times):
        row = [t]
        for v in values:
            row.append(v[i])
        rows.append(row)

    _small_writer(output_filename, rows, analyses)


def extract_best_fnc(session_id):
    fncs, fits = _extract_fnc_fits(session_id)
    return fncs, fits


def _extract_fnc_fits(session_id):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    e = session.experiments[0]

    fncs = _get_fnc_mesh(e)

    obj_bind = e.objectives['factin_fit']

    fits = []
    for fnc in fncs:
        obj_q = dbs.query(database.Objective).filter_by(bind=obj_bind)
        runs_q = obj_q.join(database.Run)
        par_q = runs_q.join(database.RunParameter).filter_by(
                name='filament_tip_concentration').filter(
                        database.RunParameter.value.like(fnc))
        best_fit = None
        for objective in par_q:
            this_fit = objective.value
            if best_fit is None or this_fit < best_fit:
                best_fit = this_fit

        fits.append(best_fit)

    return fncs, fits

#    fncs = []
#    fits = []
#    for run in e.runs:
#        fncs.append(run.all_parameters['filament_tip_concentration'])
#        objective = dbs.query(database.Objective).filter_by(run=run
#                ).filter_by(bind=obj_bind).one()
#        fits.append(objective.value)
#    return zip(sorted(zip(fncs, fits)))


def _get_fnc_mesh(experiment):
    fncs = set()
    for run in experiment.runs:
        fncs.add(run.parameters['filament_tip_concentration'])
    return sorted(list(fncs))


def _calculate_crossing_fnc(fncs, fits):
    pass

def ht_v_fil(session_id, output_filename='results/ht_v_numfil.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    rows = []
    for run in session.experiments[0].runs:
        numfils = run.all_parameters['number_of_filaments']
        halftime = run.get_objective('halftime')
        row = numfils, halftime
        rows.append(row)

    _small_writer(output_filename, sorted(rows),
            ['release rate', 'pi halftime'])

def save_fits(session_id, output_filename='results/sample_rates.dat',
        objective_name='pi_fit', parameter_name='release_rate'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    rows = []
    for run in session.experiments[0].runs:
        rate = run.parameters[parameter_name]
        fit = run.get_objective(objective_name)
        halftime = run.get_objective('halftime')
        halftime_error = run.get_objective('halftime_error')
        if fit is not None:
            rows.append((rate, fit, halftime, halftime_error))
    _small_writer(output_filename, sorted(rows),
            [parameter_name, objective_name, 'pi halftime', 'pi halftime error'])

def vectorial_save(session_id, rate_filename='results/melki_vectorial_rate.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    sample_size = (session.parameters['number_of_simulations']
            * session.parameters['number_of_filaments'])
    fractional_error = 1 / numpy.sqrt(sample_size)

    best_run = None
    best_fit = None
    for run in session.experiments[0].runs:
        run_fit = run.get_objective('pi_fit')
        if run_fit is None:
            continue
        if not best_run or best_fit > run.get_objective('pi_fit'):
            best_run = run
            best_fit = run.get_objective('pi_fit')

    best_rate = best_run.parameters['release_rate']
    statistical_error = best_rate * fractional_error
    row = ('Inf', best_rate, statistical_error,
            best_run.get_objective('halftime'),
            best_run.get_objective('halftime_error'))

    _small_writer(rate_filename, [row],
            ['rho', 'release_rate', 'naive statistical error',
                'halftime', 'halftime_error'])

def single_fnc_save(session_ids, plot_cooperativities=[1, 1000, 1000000],
        rate_filename='results/melki_rates.dat'):
#        factin_timecourse_filename='results/melki_factin_timecourses.dat',
#        pi_timecourse_filename='results/melki_pi_timecourses.dat'):
    dbs = database.DBSession()

    sessions = [dbs.query(database.Session).get(sid) for sid in session_ids]
    sessions.sort(key=lambda s: s.parameters['release_cooperativity'])

    cooperativities = [s.parameters['release_cooperativity'] for s in sessions]


    rows = []
    for rho, session in zip(cooperativities, sessions):
        sample_size = (session.parameters['number_of_simulations']
                * session.parameters['number_of_filaments'])
        fractional_error = 1 / numpy.sqrt(sample_size)

        best_run = None
        best_fit = None
        for run in session.experiments[0].runs:
            run_fit = run.get_objective('pi_fit')
            if run_fit is None:
                continue
            if not best_run or best_fit > run.get_objective('pi_fit'):
                best_run = run
                best_fit = run.get_objective('pi_fit')
        best_rate = best_run.parameters['release_rate']
        statistical_error = best_rate * fractional_error
        row = (rho, best_rate, statistical_error,
                best_run.get_objective('halftime'),
                best_run.get_objective('halftime_error'))
        rows.append(row)

    _small_writer(rate_filename, rows,
            ['release_cooperativity', 'release_rate', 'naive statistical error',
                'halftime', 'halftime_error'])
#            zip(cooperativities, rates, statistical_errors, mesh_errors, halftimes),
#            ('release_cooperativity', 'release_rate', 'statistical_error', 'mesh_error', 'halftime'),
#            header='# Filament Number Concentration: %s\n#    FNC Statistical Error: %s\n#    FNC Mesh Error: %s\n'
#            % (best_fnc, fractional_error * best_fnc, fnc_step_size / 2))


def save(session_ids, plot_cooperativities=[1, 1000, 1000000],
        rate_filename='results/melki_rates.dat',
        factin_timecourse_filename='results/melki_factin_timecourses.dat',
        pi_timecourse_filename='results/melki_pi_timecourses.dat'):
    dbs = database.DBSession()

    sessions = [dbs.query(database.Session).get(sid) for sid in session_ids]
    sessions.sort(key=lambda s: s.parameters['release_cooperativity'])

    session_rate_meshes = []
    session_pi_arrays = []
    session_fractional_errors = []

    # Collect the data and find the best FNC
    fnc_totals = None
    for session in sessions:
        session_arrays = get_session_arrays(dbs, session)
        fnc_mesh, rate_mesh, f_array, p_array, fractional_error = session_arrays

        if fnc_totals is None:
            fnc_totals = numpy.zeros(len(fnc_mesh))

        # Minimizes across all rates for the session
        fnc_totals += f_array.min(1)
        session_rate_meshes.append(rate_mesh)
        session_pi_arrays.append(p_array)
        session_fractional_errors.append(fractional_error)

    # Get the best fnc
    fnc_i = fnc_totals.argmin()
    best_fnc = fnc_mesh[fnc_i]

    # Get the best rates for each session
    cooperativities = [s.parameters['release_cooperativity'] for s in sessions]
    best_runs = []
    rates = []
    statistical_errors = []
    mesh_errors = []
    halftimes = []
    for i, (rate_mesh, pi_array, fractional_error) in enumerate(
            zip(session_rate_meshes, session_pi_arrays,
                session_fractional_errors)):
        fixed_fnc = pi_array[fnc_i, :]
        rate_i = fixed_fnc.argmin()
        rate = rate_mesh[rate_i]
        best_run = _get_best_run(dbs, sessions[i].experiments[0],
                release_rate=rate, filament_tip_concentration=best_fnc)

        try:
            step_size = rate_mesh[rate_i + 1] - rate
        except IndexError:
            print 'Index error for rho = %s' % cooperativities[i]
            step_size = 0
        rates.append(rate)
        statistical_errors.append(fractional_error * rate)
        mesh_errors.append(step_size / 2)
        best_runs.append(best_run)
        halftimes.append(best_run.get_objective('halftime'))

    try:
        fnc_step_size = fnc_mesh[fnc_i + 1] - best_fnc
    except IndexError:
        fnc_step_size = 0

    _small_writer(rate_filename,
            zip(cooperativities, rates, statistical_errors, mesh_errors, halftimes),
            ('release_cooperativity', 'release_rate', 'statistical_error', 'mesh_error', 'halftime'),
            header='# Filament Number Concentration: %s\n#    FNC Statistical Error: %s\n#    FNC Mesh Error: %s\n'
            % (best_fnc, fractional_error * best_fnc, fnc_step_size / 2))

    if plot_cooperativities:
        # Pick & write timecourses
        f_tcs = []
        pi_tcs = []
        times = []
        for pc in plot_cooperativities:
            run_i = cooperativities.index(pc)
            run = best_runs[run_i]
            times, factin, pi, f_err, pi_err = _get_timecourses(run)
            f_tcs.append(factin)
            pi_tcs.append(pi)

        factin_results = zip(times, *f_tcs)
        pi_results = zip(times, *pi_tcs)
        
        _write_results(factin_timecourse_filename, factin_results,
                'Time (s)', '[F-actin] (uM)', 'release cooperativity',
                plot_cooperativities)

        _write_results(pi_timecourse_filename, pi_results,
                'Time (s)', '[Pi] (uM)', 'release cooperativity',
                plot_cooperativities)

def _get_best_run(dbs, experiment, release_rate=None, filament_tip_concentration=None):
    fnc_alias = sqlalchemy.orm.aliased(database.RunParameter)
    rr_alias = sqlalchemy.orm.aliased(database.RunParameter)

    q = dbs.query(database.Run).filter_by(experiment=experiment)
    q = q.join((fnc_alias, fnc_alias.run_id == database.Run.id)
            ).filter_by(name='filament_tip_concentration'
            ).filter(fnc_alias.value.like(filament_tip_concentration))

    q = q.join((rr_alias, rr_alias.run_id == database.Run.id)
            ).filter_by(name='release_rate'
            ).filter(rr_alias.value.like(release_rate))

    return q.one()


def _get_timecourses(run):
    times, factin, f_err = run.analyses['factin']
    times, pi, pi_err = run.analyses['Pi']

    return times, factin, pi, f_err, pi_err


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

def _write_results(filename, rows, x_name, y_name, column_name, column_ids):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        f.write('# columns: %s\n' % column_name)
#        f.write('#     %s\n\n' % column_ids)
        f.write('#     ')
        f.write(str(column_ids))
        f.write('\n\n')
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(rows)

def get_session_arrays(db_session, session):
    session_values = _extract_session_values(db_session, session)
    fncs, rates, factin_fits, pi_fits = session_values

    fnc_mesh = sorted(list(set(fncs)))
    rate_mesh = sorted(list(set(rates)))

    f_array = numpy.zeros((len(fnc_mesh), len(rate_mesh)))
    p_array = numpy.zeros((len(fnc_mesh), len(rate_mesh)))

    for fnc, rate, f_fit, p_fit in zip(*session_values):
        fi = bisect.bisect_left(fnc_mesh, fnc)
        ri = bisect.bisect_left(rate_mesh, rate)

        f_array[fi, ri] = f_fit
        p_array[fi, ri] = p_fit

    # Figure out rough statistical error.
    sample_size = (session.parameters['number_of_simulations']
            * session.parameters['number_of_filaments'])
    fractional_error = 1 / numpy.sqrt(sample_size)


    return fnc_mesh, rate_mesh, f_array, p_array, fractional_error


def _extract_session_values(db_session, session):
    fncs = []
    rates = []
    factin_fits = []
    pi_fits = []

    e = session.experiments[0]
    fob = e.objectives['factin_fit']
    pob = e.objectives['pi_fit']

    for run in e.runs:
        fncs.append(run.all_parameters['filament_tip_concentration'])
        rates.append(run.all_parameters['release_rate'])

        fo = db_session.query(database.Objective).filter_by(run=run
                ).filter_by(bind=fob).first()
        factin_fits.append(fo.value)

        po = db_session.query(database.Objective).filter_by(run=run
                ).filter_by(bind=pob).first()
        pi_fits.append(po.value)

    return fncs, rates, factin_fits, pi_fits


def _calc_halftime(measurement, half_value):
    times, values, errors = measurement
    for i, v in enumerate(values):
        if v > half_value:
            break;

    left_time = times[i-1]
    left_value = values[i-1]

    right_time = times[i]
    right_value = values[i]

    return _interpolation.linear_project(left_value, left_time,
            right_value, right_time, half_value)
