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

from pprint import pprint

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

def timecourse_best(session, db_session):
    experiment = session.get_experiment('blanchoin_pollard_2002')
    pyrene_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['brooks_pyrene_fit'])

    best_pars = pyrene_slicer.get_best_parameters()
    print 'best pyrene pars:'
    pprint.pprint(best_pars)

    timecourse_near(session, db_session,
            filament_tip_concentration=best_pars['filament_tip_concentration'])



def timecourse_near(session, db_session, **fixed_values):
    experiment = session.get_experiment('blanchoin_pollard_2002')
    pyrene_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['brooks_pyrene_fit'])
    adppi_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['pollard_adppi_fit'])

    nearby_fixed_values = pyrene_slicer.get_nearest_values(**fixed_values)
    best_pars = adppi_slicer.get_best_parameters_near(**nearby_fixed_values)
    print 'best_adppi_pars:'
    pprint.pprint(best_pars)

    objective_id = pyrene_slicer.get_id(**best_pars)
    objective = db_session.query(database.Objective).filter_by(id=objective_id).first()

    timecourse(objective.run)

def timecourse(run, final_pyrene_value=3, theme=None):
    if not theme:
        theme = themes.Theme()

    analyses = run.analyses

    # Pyrene (sim + data)
    brooks_bind = run.experiment.objectives['brooks_pyrene_fit']
    pyrene_data = brooks_bind.measurement
    if final_pyrene_value:
        scale_factor = float(final_pyrene_value) / pyrene_data[1][-1]
    else:
        scale_factor = 1
    scaled_pyrene_data = numerical.measurements.scale(pyrene_data, scale_factor)

    brooks_objective = bindings.db_single(brooks_bind, run.all_parameters)
    brooks_fit, brooks_measurement = brooks_objective.fit_measurement(run,
            scaled_pyrene_data)

    measurements.line(brooks_measurement, label='Simulated Pyrene Intensity',
                      **theme('pyrene_dark', 'simulation_line'))

    measurements.line(scaled_pyrene_data, label='Measured Pyrene Intensity',
                      **theme('pyrene_light', 'data_line'))
    # F-Actin
    sim_factin = calculate_factin(analyses, run.all_parameters['filament_tip_concentration'])
    measurements.line(sim_factin, label='Simulated F-Actin',
                      **theme('factin_dark', 'simulation_line'))

    # ADP-Pi (sim + data)
    sim_adppi = calculate_adppi(analyses, run.all_parameters['filament_tip_concentration'])
    measurements.line(sim_adppi, label='Simulated [F-ADP-Pi-actin]',
                      **theme('adppi_dark', 'simulation_line'))
    measurements.scatter(run.experiment.objectives['pollard_adppi_fit'].measurement,
                         label='Measured [F-ADP-Pi-actin]',
                         **theme('adppi_light', 'data_points'))

    pylab.legend(loc=4)
    pylab.xlim(0, 40)
    pylab.ylim(0, 7)

# XXX Very. Sloppy.
def calculate_pyrene(analyses, filament_tip_concentration=None):
    return numerical.measurements.add([
        numerical.measurements.scale(analyses['pyrene_ATP'], 0.37 * filament_tip_concentration),
        numerical.measurements.scale(analyses['pyrene_ATP'], 0.56 * filament_tip_concentration),
        numerical.measurements.scale(analyses['pyrene_ATP'], 0.75 * filament_tip_concentration)])


def calculate_factin(analyses, filament_tip_concentration=None):
    return numerical.measurements.scale(
            numerical.measurements.add([analyses['pyrene_ATP'],
                                        analyses['pyrene_ADPPi'],
                                        analyses['pyrene_ADP']]),
            filament_tip_concentration)

def calculate_adppi(analyses, filament_tip_concentration=None):
    return numerical.measurements.scale(analyses['pyrene_ADPPi'],
                                        filament_tip_concentration)

def ftc_rate_contours(session):
    experiment = session.get_experiment('blanchoin_pollard_2002')
    pyrene_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['brooks_pyrene_fit'])
    adppi_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['pollard_adppi_fit'])

    pylab.figure()
    pylab.subplot(1,2,1)
    fit.contour(pyrene_slicer, 'filament_tip_concentration', 'cleavage_rate',
                logscale_y=True, logscale_z=True, scale_x=1000)
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.ylabel('Cleavage Rate (s^-1)')
    pylab.title('Pyrene fit')

    pylab.subplot(1,2,2)
    fit.contour(adppi_slicer, 'filament_tip_concentration', 'cleavage_rate',
                logscale_y=True, logscale_z=True, scale_x=1000)
    pylab.xlabel('Filament Tip Concentration (nM)')
    pylab.ylabel('Cleavage Rate (s^-1)')
    pylab.title('ADP-Pi fit')


def get_best_rate(session):
    experiment = session.get_experiment('blanchoin_pollard_2002')
    pyrene_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['brooks_pyrene_fit'])
    adppi_slicer = slicing.Slicer.from_objective_bind(
            experiment.objectives['pollard_adppi_fit'])

    pyrene_pars = pyrene_slicer.get_best_parameters()

    print 'Best ftc from pyrene fit:', pyrene_pars['filament_tip_concentration']

    adppi_pars = adppi_slicer.get_best_parameters_near(
            filament_tip_concentration=pyrene_pars['filament_tip_concentration'])
    print 'Best rate from adppi fit:', adppi_pars['cleavage_rate']
    pprint(adppi_pars)
