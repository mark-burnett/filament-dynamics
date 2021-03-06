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

from actin_dynamics import logger
log = logger.getLogger(__file__)

from actin_dynamics import primitives

def db_single(bind, parameters):
    registry = getattr(primitives, bind.module_name).registry
    cls = registry[bind.class_name]

    log.debug('bind: %s', bind)


    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in bind.variable_arguments.iteritems())

    kwargs = dict(var_args)
    kwargs['label'] = bind.label
    kwargs.update(bind.fixed_arguments)

    try:
        o = cls(**kwargs)
    except Exception as e:
        log.exception('Failed to instantiate binding: class_name = %s, fixed_arguments = %s, variable_arguments = %s',
                bind.class_name, bind.fixed_arguments, var_args)
        raise
    return o

def db_multiple(binds, parameters):
    results = []
    for b in binds:
        results.append(db_single(b, parameters))
    return results


def dict_single(object_dict, parameters, label, registry):
    cls = registry[object_dict['class_name']]

    kwargs = {}
    for argument_name, parameter_name in object_dict.get('variable_arguments',
                                             {}).iteritems():
        kwargs[argument_name] = parameters[parameter_name]

    kwargs['label'] = label

    fixed_pars = object_dict.get('fixed_arguments', {})
    kwargs.update(fixed_pars)

    return cls(**kwargs)

def dict_multiple(binds, parameters, registry):
    results = []
    for label, object_dict in binds.iteritems():
        results.append(dict_single(object_dict, parameters, label, registry))

    return results
