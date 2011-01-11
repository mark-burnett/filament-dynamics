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

def value_vs_parameter(analysis_container,
                       parameter_name=None,
                       analysis_name=None,
                       value_name=None):
    parameters = []
    values = []
    for parameter_set in analysis_container:
        parameters.append(parameter_set['parameters'][parameter_name])
        values.append(parameter_set[analysis_name][value_name])

    pylab.figure()
    pylab.xlabel(parameter_name)
    pylab.ylabel(value_name)

    pylab.plot(parameters, values)
    pylab.show()

#def value_vs_2_parameters(hdf_file=None,
#                          analysis_name=None,
#                          x_parameter=None,
#                          y_parameter=None,
#                          value_name=None,
#                          logscale_x=False,
#                          logscale_y=False):
#    parameter_parameter_sets, analysis = hdf.utils.get_ps_ana(hdf_file)
#    value_parameter_sets = analysis.create_or_select_child(analysis_name)
#
#    x = []
#    y = []
#    values = []
#    for ps_index in xrange(len(parameter_parameter_sets)):
#        parameter_ps = parameter_parameter_sets.select_child_number(ps_index)
#        x.append(parameter_ps.parameters[x_parameter])
#        y.append(parameter_ps.parameters[y_parameter])
#
#        value_ps = value_parameter_sets.select_child_number(ps_index)
#        values.append(value_ps.values[value_name])
#
#    points = zip(x, y, values)
#
#    pylab.figure()
#
#    pylab.xlabel(x_parameter)
#    pylab.ylabel(y_parameter)
#
#    if logscale_x:
#        pylab.semilogx()
#    if logscale_y:
#        pylab.semilogy()
#
#    pylab.contourf(points)
#    pylab.legend()
#
#    pylab.show()
