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

import collections
import numpy

import pylab

from . import utils

def values_vs_parameter(analysis_container,
                        parameter_name=None,
                        value_names=None):
    parameters = []
    values = collections.defaultdict(list)

    for parameter_set in analysis_container:
        parameters.append(parameter_set['parameters'][parameter_name])
        for value_name in value_names:
            values[value_name].append(parameter_set['values'][value_name])

    pylab.figure()
    pylab.xlabel(parameter_name)
    pylab.ylabel(', '.join(value_names))

    for name, value in values.iteritems():
        pylab.plot(parameters, value, label=name)

    pylab.legend()

    pylab.show()

def value_vs_2_parameters(analysis_container,
                          x_parameter=None,
                          y_parameter=None,
                          value_name=None,
                          logscale_x=False,
                          logscale_y=False,
                          parameter_labels=[]):
    x_values = utils.get_parameter_values(analysis_container, x_parameter)
    y_values = utils.get_parameter_values(analysis_container, y_parameter)

    z_values = numpy.zeros((len(x_values), len(y_values)))
    for parameter_set in analysis_container:
        parameters = parameter_set['parameters']
        xi = x_values.index(parameters[x_parameter])
        yi = y_values.index(parameters[y_parameter])

        z_values[xi, yi] = parameter_set['values'][value_name]

    pylab.figure()

    title = utils.parameter_title(parameters, parameter_labels)
    pylab.title(title)

    pylab.xlabel(x_parameter)
    pylab.ylabel(y_parameter)

    pylab.xlim((x_values[0], x_values[-1]))
    pylab.ylim((y_values[0], y_values[-1]))

    if logscale_x and logscale_y:
        pylab.loglog()
    elif logscale_x:
        pylab.semilogx()
    elif logscale_y:
        pylab.semilogy()

    pylab.contourf(x_values, y_values, z_values)
    pylab.colorbar()

    pylab.show()
