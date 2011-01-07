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

import itertools

import numpy

from scipy import optimize as _optimize

from actin_dynamics.io import hdf as _hdf

from actin_dynamics.analyses import downsample as _downsample

from . import utils as _utils

def fit_fluorescence_normalization(fluorescence_sim=None,
                                   fluorescence_data=None):
    # Resample the fluorescences to the data times
    times, data = fluorescence_data

    sim_times, avg, lower, upper = fluorescence_sim
    fluorescence_averages     = zip(sim_times, avg)
    fluorescence_lower_bounds = zip(sim_times, lower)
    fluorescence_upper_bounds = zip(sim_times, upper)

    fluorescences = zip(*_downsample.resample(fluorescence_averages,     times))[1]
    lower_bounds  = zip(*_downsample.resample(fluorescence_lower_bounds, times))[1]
    upper_bounds  = zip(*_downsample.resample(fluorescence_upper_bounds, times))[1]

    errors = numpy.array(upper_bounds) - numpy.array(lower_bounds)

    # Create residual function
    def model_function(normalization):
        return _chi_squared(data, fluorescences * normalization, errors)

    # Use scipy to generate the results.
    fit_results = _optimize.fmin(model_function, 1)

    return fit_results[0]

def get_fluorescence(analysis=None, parameter_set_number=None,
                     coefficients=None, normalization=1):
    # Grab the data
    times, atp_values, atp_lower_bounds, atp_upper_bounds = (
            _utils.get_measurement_summary(analysis, parameter_set_number,
                                           'pyrene_atp_count'))

    ptimes, adppi_values, adppi_lower_bounds, adppi_upper_bounds = (
            _utils.get_measurement_summary(analysis, parameter_set_number,
                                           'pyrene_adppi_count'))

    dtimes, adp_values, adp_lower_bounds, adp_upper_bounds = (
            _utils.get_measurement_summary(analysis, parameter_set_number,
                                           'pyrene_adp_count'))

    if coefficients is None:
        # XXX These may not match literature values, I can't check now.
        coefficients = {'ATP': 0.35,
                        'ADPPi': 0.56,
                        'ADP': 0.75}

    # Scale everything
    average_fluorescence = _linear_combination(
            [atp_values, adppi_values, adp_values],
            [coefficients['ATP'], coefficients['ADPPi'], coefficients['ADP']],
            normalization=normalization)

    lower_fluorescence = _linear_combination(
            [atp_lower_bounds, adppi_lower_bounds, adp_lower_bounds],
            [coefficients['ATP'], coefficients['ADPPi'], coefficients['ADP']],
            normalization=normalization)

    upper_fluorescence = _linear_combination(
            [atp_upper_bounds, adppi_upper_bounds, adp_upper_bounds],
            [coefficients['ATP'], coefficients['ADPPi'], coefficients['ADP']],
            normalization=normalization)

    return times, average_fluorescence, lower_fluorescence, upper_fluorescence


def _chi_squared(data, sim_avg, sim_std):
    return sum(((d - a) / s)**2
               for d, a, s in itertools.izip(data, sim_avg, sim_std))


def _linear_combination(values=None, coefficients=None, normalization=1):
    values = numpy.array(values).transpose()
    coefficients = numpy.array(coefficients)
    results = []
    for v in values:
        results.append(numpy.dot(v, coefficients) / normalization)
    return results
