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

import actin_dynamics

def instantiate_bind(bind, parameters, registry):
    cls = registry[bind.class_name]

    kwargs = dict((local_name, parameters[global_name])
          for local_name, global_name in bind.variable_arguments.iteritems())
    kwargs.update(dict_map)

    kwargs['label'] = bind.name
    kwargs.update(bind.fixed_arguments)

    return cls(**kwargs)

def instantiate_binds(binds, parameters):
    results = []
    for b in binds:
        results.append(instantiate_bind(b, parameters,
            getattr(actin_dynamics, b.module_name).registry))
    return results


# XXX Depracated
def instantiate_binding(object_dict, parameters, registry):
    cls = registry[object_dict['class_name']]

    par_map = {}
    dict_map = {}
    try: # NOTE getattr doesn't appear to work on yaml 'dicts' for some reason.
        for local_name, value in object_dict['parameters'].iteritems():
            try:
                temp_map = {}
                for internal_key, internal_value in value.iteritems():
                    temp_map[internal_key] = parameters[internal_value]
                dict_map[local_name] = temp_map
            except:
                par_map[local_name] = value
    except:
        pass

    kwargs = dict((local_name, parameters[global_name])
                  for local_name, global_name in par_map.iteritems())
    kwargs.update(dict_map)

    try:
        fixed_pars = object_dict['fixed_parameters']
        kwargs.update(fixed_pars)
    except:
        pass

    return cls(**kwargs)
