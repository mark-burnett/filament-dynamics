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

from . import residuals
from . import utils


def get_pyrene_fit(run, pyrene_data=None, **kwargs):
    '''
    Returns fit and normalization of pyrene simulation.
    '''
    straight_pyrene = get_unnormalized_fluorescence(run, **kwargs)

    if not pyrene_data:
        pyrene_data = io.pollard.get_interpolated_pyrene_data(straight_pyrene[0])

    return _pyrene_normalization(straight_pyrene, pyrene_data)


def get_unnormalized_fluorescence(run, atp_weight=0.37, adppi_weight=0.56,
                                       adp_weight=0.75, **kwargs):
    # Grab the simulation data
    atp_data   = run.get_measurement('pyrene_atp_count')
    adppi_data = run.get_measurement('pyrene_adppi_count')
    adp_data   = run.get_measurement('pyrene_adp_count')

    # Scale everything
    scaled_atp_data   = utils.scale_measurement(atp_data, atp_weight)
    scaled_adppi_data = utils.scale_measurement(adppi_data, adppi_weight)
    scaled_adp_data   = utils.scale_measurement(adp_data, adp_weight)

    # Add everything
    return utils.add_measurements([scaled_atp_data, scaled_adppi_data,
                                   scaled_adp_data])

def _pyrene_normalization(fluorescence_sim=None, fluorescence_data=None,
                          residual_function=residuals.naked_chi_squared):
#                          residual_function=residuals.abs_diff):
    '''
    Returns chi squared of fit and normalization parameter.
    '''
    from scipy import optimize as _optimize

    # Create residual function
    def model_function(normalization):
        scaled_sim = utils.scale_measurement(fluorescence_sim, normalization[0])

        return residual_function(fluorescence_data, scaled_sim)

    # Use scipy to generate the results.
    normalization_guess = 0.5

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[1], fit_results[0][0]
