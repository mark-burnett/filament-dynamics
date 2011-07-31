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

import numpy

from actin_dynamics import database
from actin_dynamics.io import data

#from actin_dynamics import numerical
#import actin_dynamics.numerical.measurements

#from . import slicing
#from . import fit
#from . import measurements
#from . import themes


def save_parameters(session_ids, filename='results/melki_rates.dat'):
    dbs = database.DBSession()

    sessions = [dbs.query(database.Session).get(sid) for sid in session_ids]
    sessions.sort(key=lambda s: s.parameters['release_cooperativity'])

    session_rate_meshes = []
    session_pi_arrays = []

    # Collect the data and find the best FNC
    fnc_totals = None
    for session in sessions:
        session_arrays = get_session_arrays(dbs, session)
        fnc_mesh, rate_mesh, f_array, p_array = session_arrays

        if fnc_totals is None:
            fnc_totals = numpy.zeros(len(fnc_mesh))

        # Minimizes across all rates for the session
        fnc_totals += f_array.min(1)
        session_rate_meshes.append(rate_mesh)
        session_pi_arrays.append(p_array)

    # Get the best fnc
    fnc_i = fnc_totals.argmin()
    best_fnc = fnc_mesh[fnc_i]

    # Get the best rates for each session
    cooperativities = [s.parameters['release_cooperativity'] for s in sessions]
    rates = []
    for rate_mesh, pi_array in zip(session_rate_meshes, session_pi_arrays):
        fixed_fnc = pi_array[fnc_i, :]
        pi_fit = fixed_fnc.min()
        rate_i = bisect.bisect_left(fixed_fnc, pi_fit)
        rates.append(rate_mesh[rate_i])

    _small_writer(filename, zip(cooperativities, rates),
            'release_cooperativity', 'release_rate')

def _small_writer(filename, results, x_name, y_name):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(results)

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


    return fnc_mesh, rate_mesh, f_array, p_array


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
