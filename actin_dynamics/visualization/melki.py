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

import pylab
import pprint

from actin_dynamics import database

from actin_dynamics import numerical
import actin_dynamics.numerical.measurements

from actin_dynamics.factories import bindings

from . import slicing
from . import fit
from . import measurements
from . import themes

def rate_ftc_contours(session):
    e = session.get_experiment('melki_fievez_carlier_1996')

    s_factin = slicing.Slicer.from_objective_bind(e.objectives['factin_fit'])
    s_pi     = slicing.Slicer.from_objective_bind(e.objectives['pi_fit'])

    pylab.figure()
    pylab.subplot(1, 2, 1)
    fit.contour(s_factin, 'filament_tip_concentration', 'release_rate',
                logscale_z=True, scale_x=1000)
    pylab.title('[F-actin] fit')
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.ylabel('Release Rate (s^-1)')

    pylab.subplot(1, 2, 2)
    fit.contour(s_pi, 'filament_tip_concentration', 'release_rate',
                logscale_z=True, scale_x=1000)
    pylab.title('[Pi] fit')
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.ylabel('Release Rate (s^-1)')

def get_best_pars(session, **extra_pars):
    e = session.get_experiment('melki_fievez_carlier_1996')

    s_factin = slicing.Slicer.from_objective_bind(e.objectives['factin_fit'])
    s_pi     = slicing.Slicer.from_objective_bind(e.objectives['pi_fit'])

    factin_pars = s_factin.get_best_parameters()

    ftc = factin_pars['filament_tip_concentration']

    pi_pars = s_pi.get_best_parameters_near(filament_tip_concentration=ftc,
                                            **extra_pars)
#    pi_pars = s_pi.get_best_parameters_near(**extra_pars)

    return pi_pars

def print_best_pars(session):
    pars = get_best_pars(session)
    ftc = pars['filament_tip_concentration']
    print 'Best ftc from f-actin fit:', ftc
    print 'Best rate from pi fit:', pars['release_rate']
    pprint.pprint(pars)

def best_timecourse(session, theme=None, **extra_pars):
    best_pars = get_best_pars(session, **extra_pars)
    pprint.pprint(best_pars)

    pylab.figure()

    e = session.get_experiment('melki_fievez_carlier_1996')
    ob_factin = e.objectives['factin_fit']
    ob_pi     = e.objectives['pi_fit']

    s_factin = slicing.Slicer.from_objective_bind(ob_factin)

    objective_id = s_factin.get_id(**best_pars)

    db_session = database.DBSession()
    objective = db_session.query(database.Objective
            ).filter_by(id=objective_id).first()

    if not theme:
        theme = themes.Theme()

    run = objective.run
    parameters = run.all_parameters
    analyses = run.analyses

    measurements.line(analyses['factin'], label='[F-actin] - Simulated',
                      **theme('factin_dark', 'simulation_line'))
    measurements.line(ob_factin.measurement, label='[F-actin] - Data',
                      **theme('factin_light', 'data_line'))

    measurements.line(analyses['Pi'], label='[Pi] - Simulated',
                      **theme('pi_dark', 'simulation_line'))
    last_data_value = ob_pi.measurement[1][-1]
    scaled_pi = numerical.measurements.scale(ob_pi.measurement,
            analyses['Pi'][1][-1] / last_data_value)
    measurements.line(scaled_pi, label='[Pi] - Data',
                      **theme('pi_light', 'data_line'))

    pylab.xlim(0, 2500)
    pylab.ylim(0, 35)
    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

    pylab.title('Rho_r = %s, r_r = %s, ftc = %s' %(
                parameters['release_cooperativity'],
                parameters['release_rate'],
                parameters['filament_tip_concentration']))

#    pylab.title('r_tip = %s, r_r = %s, ftc = %s' %(
#                best_pars['tip_phosphate_release'],
#                best_pars['release_rate'],
#                best_pars['filament_tip_concentration']))

    pylab.legend(loc=4)
