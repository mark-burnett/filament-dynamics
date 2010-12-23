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

from actin_dynamics.io import hdf as _hdf

from actin_dynamics.analyses import downsample as _downsample

from . import utils as _utils

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

def fit_fluorescence(simulation_fluorescence, data_fluorescence):
    sim_times, sim_avg, sim_lower, sim_upper = simulation_fluorescence
    data_times, data_avg = data_fluorescence

    sim_std = [(u - l)/2 for l, u in itertools.izip(sim_lower, sim_upper)]
    junk_times, sampled_avg = zip(*_downsample.resample(zip(sim_times, sim_avg), data_times))
    junk_times, sampled_std = zip(*_downsample.resample(zip(sim_times, sim_std), data_times))

    return _chi_squared(data_avg, sampled_avg, sampled_std) / len(data_avg)


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

def normalize_fluorescence(length_measurement, fluorescence_measurement):
    tl, al, ll, ul = length_measurement
    tf, af, lf, uf = fluorescence_measurement

    scale_factor = al[-1] / af[-1]

    new_average     = [f * scale_factor for f in af]
    new_lower_bound = [f * scale_factor for f in lf]
    new_upper_bound = [f * scale_factor for f in uf]

    return tf, new_average, new_lower_bound, new_upper_bound
