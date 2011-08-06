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

#import pylab
#import pprint

import bisect
import csv

import sqlalchemy
import numpy

from actin_dynamics import database
from actin_dynamics.io import data

#from actin_dynamics import numerical
#import actin_dynamics.numerical.measurements

#from . import slicing
#from . import fit
#from . import measurements
#from . import themes

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
    for i, (rate_mesh, pi_array, fractional_error) in enumerate(zip(session_rate_meshes,
            session_pi_arrays, session_fractional_errors)):
        fixed_fnc = pi_array[fnc_i, :]
        rate_i = fixed_fnc.argmin()
        rate = rate_mesh[rate_i]
        best_run = _get_best_run(dbs, sessions[i].experiments[0], release_rate=rate, filament_tip_concentration=best_fnc)

        try:
            assert rate == best_run.all_parameters['release_rate']
        except AssertionError:
            print 'run parameters', best_run.parameters
            print 'Pi objectives:'
            print fixed_fnc
            print 'best index:', rate_i
            print 'rate mesh:'
            print numpy.array(rate_mesh)
            print 'expected rate:', rate, 'actual rate:', best_run.all_parameters['release_rate']

        try:
            step_size = rate_mesh[rate_i + 1] - rate
        except IndexError:
            print 'Index error for rho = %s' % cooperativities[i]
            step_size = 0
        rates.append(rate)
        statistical_errors.append(fractional_error * rate)
        mesh_errors.append(step_size / 2)
        best_runs.append(best_run)

    fnc_step_size = fnc_mesh[fnc_i + 1] - best_fnc
    _small_writer(rate_filename,
            zip(cooperativities, rates, statistical_errors, mesh_errors),
            ('release_cooperativity', 'release_rate', 'statistical_error', 'mesh_error'),
            header='# Filament Number Concentration: %s\n#    FNC Statistical Error: %s\n#    FNC Mesh Error: %s\n'
            % (best_fnc, fractional_error * best_fnc, fnc_step_size / 2))

    # Pick & write timecourses
    f_tcs = []
    pi_tcs = []
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
        f.write('#     %s\n\n' % column_ids)
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


#def rate_ftc_contours(session):
#    e = session.get_experiment('melki_fievez_carlier_1996')
#
#    s_factin = slicing.Slicer.from_objective_bind(e.objectives['factin_fit'])
#    s_pi     = slicing.Slicer.from_objective_bind(e.objectives['pi_fit'])
#
#    pylab.figure()
#    pylab.subplot(1, 2, 1)
#    fit.contour(s_factin, 'filament_tip_concentration', 'release_rate',
#                logscale_z=True, scale_x=1000)
#    pylab.title('[F-actin] fit')
#    pylab.xlabel('Filament Tip Concentration (nM)')
#    pylab.ylabel('Release Rate (s^-1)')
#
#    pylab.subplot(1, 2, 2)
#    fit.contour(s_pi, 'filament_tip_concentration', 'release_rate',
#                logscale_z=True, scale_x=1000)
#    pylab.title('[Pi] fit')
#    pylab.xlabel('Filament Tip Concentration (nM)')
#    pylab.ylabel('Release Rate (s^-1)')
#
#def get_best_pars(session, **extra_pars):
#    e = session.get_experiment('melki_fievez_carlier_1996')
#
#    s_factin = slicing.Slicer.from_objective_bind(e.objectives['factin_fit'])
#    s_pi     = slicing.Slicer.from_objective_bind(e.objectives['pi_fit'])
#
#    factin_pars = s_factin.get_best_parameters()
#
#    ftc = factin_pars['filament_tip_concentration']
#
#    pi_pars = s_pi.get_best_parameters_near(filament_tip_concentration=ftc,
#                                            **extra_pars)
##    pi_pars = s_pi.get_best_parameters_near(**extra_pars)
#
#    return pi_pars
#
#def print_best_pars(session):
#    pars = get_best_pars(session)
#    ftc = pars['filament_tip_concentration']
#    print 'Best ftc from f-actin fit:', ftc
#    print 'Best rate from pi fit:', pars['release_rate']
#    pprint.pprint(pars)
#
#def best_timecourse(session, theme=None, **extra_pars):
#    best_pars = get_best_pars(session, **extra_pars)
#    pprint.pprint(best_pars)
#
#    pylab.figure()
#
#    e = session.get_experiment('melki_fievez_carlier_1996')
#    ob_factin = e.objectives['factin_fit']
#    ob_pi     = e.objectives['pi_fit']
#
#    s_factin = slicing.Slicer.from_objective_bind(ob_factin)
#
#    objective_id = s_factin.get_id(**best_pars)
#
#    db_session = database.DBSession()
#    objective = db_session.query(database.Objective
#            ).filter_by(id=objective_id).first()
#
#    if not theme:
#        theme = themes.Theme()
#
#    run = objective.run
#    parameters = run.all_parameters
#    analyses = run.analyses
#
#    measurements.line(analyses['factin'], label='[F-actin] - Simulated',
#                      **theme('factin_dark', 'simulation_line'))
#    measurements.line(ob_factin.measurement, label='[F-actin] - Data',
#                      **theme('factin_light', 'data_line'))
#
#    measurements.line(analyses['Pi'], label='[Pi] - Simulated',
#                      **theme('pi_dark', 'simulation_line'))
#    last_data_value = ob_pi.measurement[1][-1]
#    scaled_pi = numerical.measurements.scale(ob_pi.measurement,
#            analyses['Pi'][1][-1] / last_data_value)
#    measurements.line(scaled_pi, label='[Pi] - Data',
#                      **theme('pi_light', 'data_line'))
#
#    pylab.xlim(0, 2500)
#    pylab.ylim(0, 35)
#    pylab.xlabel('Time (s)')
#    pylab.ylabel('Concentration (uM)')
#
#    pylab.title('Rho_r = %s, r_r = %s, ftc = %s' %(
#                parameters['release_cooperativity'],
#                parameters['release_rate'],
#                parameters['filament_tip_concentration']))
#
##    pylab.title('r_tip = %s, r_r = %s, ftc = %s' %(
##                best_pars['tip_phosphate_release'],
##                best_pars['release_rate'],
##                best_pars['filament_tip_concentration']))
#
#    pylab.legend(loc=4)
