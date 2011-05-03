#    Copyright (C) 2010-2011 Mark Burnett
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

from actin_dynamics import primitives


def instantiate_from_db(binding=None, parameters={}):
    return instantiate_from_dict(parameters=parameters,
                                 **binding.to_dict())

def instantiate_multiple_from_db(bindings, parameters):
    f = lambda b: from_db(b, parameters)
    return map(f, bindings)


def instantiate_from_dict(parameters=None, module_name=None, label=None,
        class_name=None, fixed_arguments=None, variable_arguments=None):
    cls = getattr(primitives, module_name).registry['class_name']

    kwargs = {}
    for argument_name, parameter_name in variable_arguments.iteritems():
        kwargs[argument_name] = parameters[parameter_name]

    kwargs['label'] = label

    kwargs.update(fixed_arguments)

    return cls(**kwargs)

def instantiate_multiple_from_dict(object_dicts, parameters={}):
    results = []
    for label, obj in object_dicts.iteritems():
        results.append(instantiate_from_dict(parameters=parameters,
                                             label=label, **obj))
    return results
