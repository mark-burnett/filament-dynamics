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
from . import residuals as _residuals
from . import utils as _utils

from actin_dynamics import io

def get_data(pyrene_filename='data/pollard_2002/pyrene_fluorescence.dat',
             adppi_filename='data/pollard_2002/adppi_concentration.dat'):
    pyrene_data = io.data.load_data(pyrene_filename)
    adppi_data  = io.data.load_data(adppi_filename)

    # Resample the fluorescence data.
    sample_times = range(41)
    resampled_pyrene_data = _interpolation.resample_measurement(pyrene_data,
                                                                sample_times)
    return [resampled_pyrene_data, adppi_data]


def pyrene_fit(parameter_set, data, **kwargs):
    sim_results = get_fluorescence(parameter_set['sem'], **kwargs)
    nx2_norm, nx2_fit = fit_normalization(sim_results, data,
            residual_function=_residuals.naked_chi_squared)

    return nx2_fit


def adppi_fit(parameter_set, data, **kwargs):
    ftc = parameter_set['parameters']['filament_tip_concentration']
    sample_times = data[0]

    # Get and resample simulation results
    # XXX We are only using pyrene adppi, we should be using both.
    raw_sim_data = parameter_set['sem']['pyrene_adppi_count']
    sampled_sim_data = _interpolation.resample_measurement(
            raw_sim_data, sample_times)
    scaled_sim_data = _utils.scale_measurement(sampled_sim_data, ftc)

    return _residuals.naked_chi_squared(scaled_sim_data, data)


def fluorescence_fit(parameter_set, data, coefficients=None):
    # Calculate fluorescence curve.
    sim_results = get_fluorescence(parameter_set['sem'],
                                   coefficients=coefficients)

    x2_norm, x2_fit = fit_normalization(sim_results, data,
            residual_function=_residuals.chi_squared)
    sim_x2 = _utils.scale_measurement(sim_results, x2_norm)

    parameter_set['pollard']['pyrene_fit_chi_squared'] = x2_fit
    parameter_set['sem']['pyrene_fit_chi_squared'] = sim_x2

    ad_norm, ad_fit = fit_normalization(sim_results, data,
            residual_function=_residuals.average_divided)
    sim_ad = _utils.scale_measurement(sim_results, ad_norm)

    parameter_set['pollard']['pyrene_fit_average_divided'] = ad_fit
    parameter_set['sem']['pyrene_fit_average_divided'] = sim_ad

    nx2_norm, nx2_fit = fit_normalization(sim_results, data,
            residual_function=_residuals.naked_chi_squared)
    sim_nx2 = _utils.scale_measurement(sim_results, nx2_norm)

    parameter_set['pollard']['pyrene_fit_naked_chi_squared'] = nx2_fit
    parameter_set['sem']['pyrene_fit_naked_chi_squared'] = sim_nx2


def get_fluorescence(parameter_set, atp_weight=0.37, adppi_weight=0.56,
                     adp_weight=0.75, **kwargs):
    '''
    Gives the unnormalized pyrene fluorescence.

    parameter_set is the 'average' analysis parameter set
    '''
    # Grab the simulation data
    atp_data   = parameter_set['pyrene_atp_count']
    adppi_data = parameter_set['pyrene_adppi_count']
    adp_data   = parameter_set['pyrene_adp_count']

    # Scale everything
    scaled_atp_data   = _utils.scale_measurement(atp_data, atp_weight)
    scaled_adppi_data = _utils.scale_measurement(adppi_data, adppi_weight)
    scaled_adp_data   = _utils.scale_measurement(adp_data, adp_weight)

    # Add everything
    return _utils.add_measurements(scaled_atp_data, scaled_adppi_data,
                                   scaled_adp_data)


def fit_normalization(fluorescence_sim=None, fluorescence_data=None,
                      residual_function=_residuals.naked_chi_squared):
    '''
    Returns normalization parameter and chi squared of fit.
    '''
    from scipy import optimize as _optimize

    # Create residual function
    def model_function(normalization):
        if normalization[0] <= 0:
            return 5000
        scaled_sim = _utils.scale_measurement(fluorescence_sim,
                                              normalization[0])
        cs = residual_function(fluorescence_data, scaled_sim)
        return cs

    # Use scipy to generate the results.
    times, data = fluorescence_data
    stimes, sim_avg, sim_error = fluorescence_sim
    normalization_guess = data[-1] / sim_avg[-1]

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[0][0], fit_results[1]


def old_adppi_fit(parameter_set, data, source='sem'):
    ftc = parameter_set['parameters']['filament_tip_concentration']
    sample_times = data[0]

    # Get and resample simulation results
    # XXX We are only using pyrene adppi, we should be using both.
    raw_sim_data = parameter_set[source]['pyrene_adppi_count']
    sampled_sim_data = _interpolation.resample_measurement(
            raw_sim_data, sample_times)
    scaled_sim_data = _utils.scale_measurement(sampled_sim_data, ftc)

    x2       = _residuals.chi_squared(scaled_sim_data, data)
    avg_div  = _residuals.average_divided(scaled_sim_data, data)
    naked_x2 = _residuals.naked_chi_squared(scaled_sim_data, data)

    parameter_set['pollard']['adppi_fit_chi_squared'] = x2
    parameter_set['pollard']['adppi_fit_average_divided'] = avg_div
    parameter_set['pollard']['adppi_fit_naked_chi_squared'] = naked_x2
