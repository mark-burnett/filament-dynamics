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

from . import downsample as _downsample
from . import stats as _stats

from actin_dynamics.io import hdf as _hdf

def perform_all(hdf_file=None):
    simulations_group = hdf_file.getNode('/Simulations')
    analysis_group = _hdf.utils.get_or_create_group(hdf_file, 'Analysis',
            description='Analysis of simulation results.')

    # Remove old analysis.
    analysis_group._f_remove(recursive=True)
    analysis_group = _hdf.utils.get_or_create_group(hdf_file, 'Analysis',
            description='Analysis of simulation results.')

    parameter_sets_wrapper = _hdf.MultipleParameterSetWrapper(simulations_group)

    analyses_wrapper = _hdf.MultipleAnalysisWrapper(analysis_group)

    downsample_analysis_wrapper = analyses_wrapper.create_child('downsample')
    _downsample.all_measurements(parameter_sets_wrapper,
                                 downsample_analysis_wrapper)

    average_analaysis_wrapper = analyses_wrapper.create_child('average')
    _stats.average_all(downsample_analysis_wrapper, average_analaysis_wrapper)

    std_analaysis_wrapper = analyses_wrapper.create_child('standard_deviation')
    _stats.std_all(downsample_analysis_wrapper, std_analaysis_wrapper)
