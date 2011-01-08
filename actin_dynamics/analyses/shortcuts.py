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

import numpy as _numpy

from scipy import interpolate as _interpolate

from . import downsample as _downsample
from . import fluorescence as _fluorescence
from . import stats as _stats

from actin_dynamics.io import hdf as _hdf
from actin_dynamics.io import data as _dataio

def perform_common(hdf_file=None):
    simulations_group = hdf_file.getNode('/Simulations')
    analysis_group = _hdf.utils.get_or_create_group(hdf_file, 'Analysis',
            description='Analysis of simulation results.')
    analyses_wrapper = _hdf.MultipleAnalysisWrapper(analysis_group)

    # Clean up old stuff.
    analyses_wrapper.delete_children()

    parameter_sets_wrapper = _hdf.MultipleParameterSetWrapper(simulations_group)

    downsample_analysis_wrapper = analyses_wrapper.create_child('downsample')
    _downsample.all_measurements(parameter_sets_wrapper,
                                 downsample_analysis_wrapper)

    average_analaysis_wrapper = analyses_wrapper.create_child('average')
    _stats.average_all(downsample_analysis_wrapper, average_analaysis_wrapper)

    std_analaysis_wrapper = analyses_wrapper.create_child('standard_deviation')
    _stats.std_all(downsample_analysis_wrapper, std_analaysis_wrapper)

def perform_pollard(hdf_file=None, fluorescence_filename='pollard_length.dat'):
    # Load (and resample) the data.
    raw_times, raw_data = _dataio.load_data(fluorescence_filename)

    sample_times = range(41)
    interp = _interpolate.InterpolatedUnivariateSpline(
            raw_times, raw_data, bbox=[0, 40])
    fluorescence_values = interp(sample_times)
    fluorescence_data = sample_times, fluorescence_values

    # Do the work.
    simulations, analysis = _hdf.utils.get_ps_ana(hdf_file)

    # Pyrene fluorescence
    fluorescence_sets = analysis.create_or_select_child('fluorescence')
    _fluorescence.all_measurements(analysis.average, fluorescence_sets,
                                   fluorescence_data)
