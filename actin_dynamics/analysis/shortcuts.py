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

from . import downsample as _downsample
from . import interpolation as _interpolation
from . import pollard as _pollard
from . import standard_error_of_mean as _standard_error_of_mean

from actin_dynamics.io import data as _dataio


def perform_common(simulation_container):
    '''
    Creates a new analysis container based on the simulations provided.
    '''
    return map(perform_common_single, simulation_container)


def perform_common_single(parameter_set):
    analyses = {}
    analyses['parameters'] = parameter_set['parameters']
    downsampled_results = _downsample.all_measurements(parameter_set)
    analyses['downsampled'] = downsampled_results

    analyses['sem'] = _standard_error_of_mean.all_measurements(
            downsampled_results)

    return analyses


def perform_pollard(analysis_container,
                    fluorescence_filename='pollard_length.dat',
                    adppi_filename='pollard_cleavage.dat'):
    '''
    Appends new analysis to the provided container.
    '''
    # Load the data.
    fluor_measurement = _dataio.load_data(fluorescence_filename)
    adppi_data = _dataio.load_data(adppi_filename)

    # Resample the fluorescence data.
    sample_times = range(41)
    fluorescence_data = _interpolation.resample_measurement(fluor_measurement,
                                                            sample_times)

    # Do the work.
    for parameter_set in analysis_container:
        parameter_set['values'] = {}
        _pollard.fluorescence_fit(parameter_set, fluorescence_data)
        _pollard.adppi_fit(parameter_set, adppi_data)
