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
import itertools
import numpy
import math

import pylab

from . import utils

def values_vs_parameter(analysis_container,
                        parameter_name=None,
                        value_names=None,
                        plot_labels=None):
    value_dicts = [dict() for vn in value_names]

    for parameter_set in analysis_container:
        for value_name, val_dict in itertools.izip(value_names,
                                                   value_dicts):
            par_value = parameter_set['parameters'][parameter_name]
            value = parameter_set['values'][value_name]
            val_dict[par_value] = min(value, val_dict.get(par_value, value))

    parameters  = sorted(value_dicts[0].keys())
    value_lists = [[val_dict[p] for p in parameters]
                   for val_dict in value_dicts]

    if plot_labels is None:
        plot_labels = value_names

    # XXX also print total
    for name, values in itertools.izip(plot_labels, value_lists):
        pylab.plot(parameters, values, label=name)

def value_vs_2_parameters(analysis_container,
                          x_parameter=None,
                          y_parameter=None,
                          value_name=None,
                          logscale_x=False,
                          logscale_y=False,
                          parameter_labels=[]):
    x_values = utils.get_parameter_values(analysis_container, x_parameter)
    y_values = utils.get_parameter_values(analysis_container, y_parameter)

    z_values = -numpy.ones((len(x_values), len(y_values)))
    for parameter_set in analysis_container:
        parameters = parameter_set['parameters']
        xi = x_values.index(parameters[x_parameter])
        yi = y_values.index(parameters[y_parameter])

        current_value = math.log(parameter_set['values'][value_name])
        if -1 == z_values[xi, yi]:
            z_values[xi, yi] = current_value
        else:
            z_values[xi, yi] = min(current_value, z_values[xi, yi])

    pylab.figure()

    title = utils.parameter_title(parameters, parameter_labels)
    pylab.title(title)

    pylab.xlabel(y_parameter)
    pylab.ylabel(x_parameter)

#    pylab.xlim((x_values[0], x_values[-1]))
#    pylab.ylim((y_values[0], y_values[-1]))

    if logscale_x and logscale_y:
        pylab.loglog()
    elif logscale_x:
        pylab.semilogx()
    elif logscale_y:
        pylab.semilogy()

    print len(x_values), len(y_values)
    print z_values.shape

#    pylab.contourf(x_values, y_values, z_values)
    pylab.contourf(y_values, x_values, z_values)
#    pylab.contourf(z_values)
    pylab.colorbar()

    pylab.show()
