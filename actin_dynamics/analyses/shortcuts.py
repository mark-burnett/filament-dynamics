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

from . import concentrations as _concentrations
from . import downsample as _downsample
from . import interpolation as _interpolation
from . import fluorescence as _fluorescence
from . import standard_error_of_mean as _standard_error_of_mean

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

    sem_analysis_wrapper = analyses_wrapper.create_child('sem')
    _standard_error_of_mean.all_measurements(downsample_analysis_wrapper,
                                             sem_analysis_wrapper)

def perform_pollard(hdf_file=None,
                    fluorescence_filename='pollard_length.dat',
                    adppi_filename='pollard_cleavage.dat'):
    # Load the data.
    fluor_measurement = _dataio.load_data(fluorescence_filename)
    adppi_data = _dataio.load_data(adppi_filename)

    # Resample the fluorescence data.
    sample_times = range(41)
    fluorescence_data = _interpolation.resample_measurement(fluor_measurement,
                                                            sample_times)

    # Do the work.
    simulations, analysis = _hdf.utils.get_ps_ana(hdf_file)

    # Pyrene fluorescence
    pollard_results = analysis.create_or_select_child('pollard')
    pollard_results.delete_children()
    _fluorescence.all_measurements(analysis.sem, pollard_results,
                                   fluorescence_data)

    # ADPPi concentration
    _concentrations.adppi_fit(simulations=simulations,
                              input_parameter_sets=analysis.sem,
                              output_parameter_sets=pollard_results, 
                              data=adppi_data)
