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

#from actin_dynamics.common import logutils
#logger = logutils.getLogger(__file__)

def instantiate_binding(parameter_value_map, binding, registry):
    cls = registry[binding.class_name]

    parameter_name_map = _make_parameter_name_map(binding.parameter_mappings)
    state_map = _make_state_map(binding.state_mappings)

    kwargs = state_map
    kwargs.update(_make_parameter_kwargs(parameter_value_map, parameter_name_map,
                                         cls.parameters))
#    logger.debug('Instantiating binding: %s' % binding)
    return cls(**_kwargs_to_ascii(kwargs))

def _make_parameter_kwargs(parameter_value_map, parameter_name_map, parameters):
    kwargs = {}
    for par_name in parameters:
        kwargs[par_name] = parameter_value_map[parameter_name_map[par_name]]
    return kwargs

def _kwargs_to_ascii(kwargs):
    return dict((str(k), v) for k, v in kwargs.iteritems())


def _make_parameter_name_map(parameter_mappings):
    return dict((pm.local_name, pm.parameter_label) for pm in parameter_mappings)

def _make_state_map(state_mappings):
    return dict((m.local_name, m.state) for m in state_mappings)
