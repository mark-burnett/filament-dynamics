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

from . import interpolation as _interpolation
from . import fitting as _fitting
from . import utils as _utils

def fluorescence_fit(parameter_set, data, coefficients=None):
    # Calculate fluorescence curve.
    sim_results = get_fluorescence(parameter_set['sem'],
                                   coefficients=coefficients)
    normalization, fluor_fit = fit_normalization(sim_results, data)
    norm_simulation = _utils.scale_measurement(sim_results, normalization)

    # Write fluorescence
    parameter_set['sem']['pyrene_fluorescence'] = norm_simulation

    # Write goodness of fit.
    parameter_set['values']['fluorescence_fit'] = fluor_fit


def get_fluorescence(parameter_set, coefficients=None):
    '''
    Gives the unnormalized pyrene fluorescence.

    parameter_set is the 'average' analysis parameter set
    Assumes standard sqrt(N) error.
    '''
    # Grab the simulation data
    atp_data   = parameter_set['pyrene_atp_count']
    adppi_data = parameter_set['pyrene_adppi_count']
    adp_data   = parameter_set['pyrene_adp_count']

    if coefficients is None:
        coefficients = {'atp':   0.37,
                        'adppi': 0.56,
                        'adp':   0.75}

    # Scale everything
    scaled_atp_data   = _utils.scale_measurement(atp_data, coefficients['atp'])
    scaled_adppi_data = _utils.scale_measurement(adppi_data,
                                                 coefficients['adppi'])
    scaled_adp_data   = _utils.scale_measurement(adp_data, coefficients['adp'])

    # Add everything
    return _utils.add_measurements(scaled_atp_data, scaled_adppi_data,
                                   scaled_adp_data)


def fit_normalization(fluorescence_sim=None, fluorescence_data=None):
    '''
    Returns normalization parameter and chi squared of fit.
    '''
    from scipy import optimize as _optimize

    # Create residual function
    def model_function(normalization):
        if normalization[0] <= 0:
            return 5000
        scaled_sim = _utils.scale_measurement(fluorescence_sim, normalization[0])
        cs = _fitting.measurement_other(fluorescence_data, scaled_sim)
        return cs

    # Use scipy to generate the results.
    times, data = fluorescence_data
    stimes, sim_avg, sim_error = fluorescence_sim
    normalization_guess = data[-1] / sim_avg[-1]

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[0][0], fit_results[1]


def adppi_fit(parameter_set, data, source='sem'):
    ftc = parameter_set['parameters']['filament_tip_concentration']
    sample_times = data[0]

    # Get and resample simulation results
    # XXX We are only using pyrene adppi, we should be using both.
    raw_sim_data = parameter_set[source]['pyrene_adppi_count']
    sampled_sim_data = _interpolation.resample_measurement(
            raw_sim_data, sample_times)
    scaled_sim_data = _utils.scale_measurement(sampled_sim_data, ftc)

    fit_quality = _fitting.measurement_other(scaled_sim_data, data)

    parameter_set['values']['adppi_fit'] = fit_quality
