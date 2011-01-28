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

from actin_dynamics import io

from . import interpolation
from . import residuals
from . import utils


def get(parameter_set, name):
    return parameter_set['sem'][name]

def get_length(parameter_set):
    basic_length = parameter_set['sem']['length']
    subtracted_length = utils.add_number(basic_length,
            -basic_length[1][0])
    return utils.scale_measurement(subtracted_length,
            parameter_set['parameters']['filament_tip_concentration'])

def get_scaled(parameter_set, name):
    basic = parameter_set['sem'][name]
    return utils.scale_measurement(basic,
            parameter_set['parameters']['filament_tip_concentration'])


def get_fluorescence(parameter_set, **kwargs):
    straight_pyrene = get_unnormalized_fluorescence(parameter_set, **kwargs)
    pyrene_data, adppi_data = io.pollard.get_data()

    interpolated_pyrene = interpolation.resample_measurement(
            pyrene_data, straight_pyrene[0])

    norm, fit = _pyrene_normalization(straight_pyrene, interpolated_pyrene)

    return utils.scale_measurement(straight_pyrene, norm)


def get_unnormalized_fluorescence(parameter_set,
                                  atp_weight=0.37, adppi_weight=0.56,
                                  adp_weight=0.75, **kwargs):
    # Grab the simulation data
    atp_data   = parameter_set['sem']['pyrene_atp_count']
    adppi_data = parameter_set['sem']['pyrene_adppi_count']
    adp_data   = parameter_set['sem']['pyrene_adp_count']

    # Scale everything
    scaled_atp_data   = utils.scale_measurement(atp_data, atp_weight)
    scaled_adppi_data = utils.scale_measurement(adppi_data, adppi_weight)
    scaled_adp_data   = utils.scale_measurement(adp_data, adp_weight)

    # Add everything
    return utils.add_measurements([scaled_atp_data, scaled_adppi_data,
                                   scaled_adp_data])

def _pyrene_normalization(fluorescence_sim=None, fluorescence_data=None,
                          residual_function=residuals.naked_chi_squared):
    '''
    Returns normalization parameter and chi squared of fit.
    '''
    from scipy import optimize as _optimize

    # Create residual function
    def model_function(normalization):
#        if normalization[0] <= 0:
#            return 5000000
        scaled_sim = utils.scale_measurement(fluorescence_sim, normalization[0])

        return residual_function(fluorescence_data, scaled_sim)

    # Use scipy to generate the results.
    normalization_guess = 1

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[0][0], fit_results[1]
