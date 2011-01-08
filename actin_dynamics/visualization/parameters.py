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

import pylab

from actin_dynamics.io import hdf


def value_vs_parameter(hdf_file=None,
                       analysis_name=None,
                       parameter_name=None,
                       value_name=None,
                       *args, **kwargs):
    '''
    Additional args and keyword args are passed on to pylab.plot()
    '''
    parameter_parameter_sets, analysis = hdf.utils.get_ps_ana(hdf_file)
    value_parameter_sets = analysis.create_or_select_child(analysis_name)

    parameters = []
    values = []
    for ps_index in xrange(len(parameter_parameter_sets)):
        parameter_ps = parameter_parameter_sets.select_child_number(ps_index)
        parameters.append(parameter_ps.parameters[parameter_name])

        value_ps = value_parameter_sets.select_child_number(ps_index)
        values.append(value_ps.values[value_name])

    pylab.plot(parameters, values)
    pylab.show()
