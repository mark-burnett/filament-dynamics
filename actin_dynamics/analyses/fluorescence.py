#    Copyright (C) 2010 Mark Burnett
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

import numpy

from scipy import optimize as _optimize

from . import fitting as _fitting
from . import utils as _utils

def all_measurements(input_parameter_sets, output_parameter_sets, data,
                     coefficients=None):
    for input_ps in input_parameter_sets:
        # Calculate fluorescence curve.
        simulation = get_fluorescence(input_ps, coefficients=coefficients)
        normalization, chi_squared = fit_normalization(simulation, data)
        norm_simulation = _utils.scale_measurement(simulation, normalization)

        # Write fluorescence
        output_ps = output_parameter_sets.create_or_select_child(input_ps.name)
        output_measurement = output_ps.measurement_summary.create_or_select_child(
                'pyrene_fluorescence')
        output_measurement.write(zip(*norm_simulation[:2]))
        error_measurement = output_ps.measurement_summary.create_or_select_child(
                'pyrene_fluorescence_error')
        error = zip(norm_simulation[0], norm_simulation[2])
        error_measurement.write(error)

        # Write fluorescence_chi_squared.
        output_ps.values['fluorescence_chi_squared'] = chi_squared


def get_fluorescence(parameter_set=None, coefficients=None):
    '''
    Gives the unnormalized pyrene fluorescence.

    parameter_set is the 'average' analysis parameter set
    Assumes standard sqrt(N) error.
    '''
    # Grab the simulation data
    atp_data   = _utils.get_measurement(parameter_set, 'pyrene_atp_count')
    adppi_data = _utils.get_measurement(parameter_set, 'pyrene_adppi_count')
    adp_data   = _utils.get_measurement(parameter_set, 'pyrene_adp_count')

    if coefficients is None:
        # XXX These may not match literature values, I can't check now.
        coefficients = {'atp':   0.35,
                        'adppi': 0.56,
                        'adp':   0.75}

    # Scale everything
    scaled_atp_data   = _utils.scale_measurement(atp_data, coefficients['atp'])
    scaled_adppi_data = _utils.scale_measurement(adppi_data, coefficients['adppi'])
    scaled_adp_data   = _utils.scale_measurement(adp_data, coefficients['adp'])

    # Add everything
    return _utils.add_measurements(scaled_atp_data, scaled_adppi_data,
                                   scaled_adp_data)


def fit_normalization(fluorescence_sim=None, fluorescence_data=None):
    '''
    Returns normalization parameter and chi squared of fit.
    '''
    sv = numpy.array(fluorescence_sim[1])
    dv = numpy.array(fluorescence_data[1])

    # Create residual function
    def model_function(normalization):
        if normalization[0] <= 0:
            return 5000
        scaled_sim = _utils.scale_measurement(fluorescence_sim, normalization[0])
#        cs = _fitting.measurement_chi_squared(fluorescence_data, scaled_sim)
        cs = _fitting.measurement_other(fluorescence_data, scaled_sim)
        return cs

    # Use scipy to generate the results.
    times, data = fluorescence_data
    stimes, sim_avg, sim_error = fluorescence_sim
    normalization_guess = data[-1] / sim_avg[-1]

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[0][0], fit_results[1]
