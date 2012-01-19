#    Copyright (C) 2012 Mark Burnett
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

from actin_dynamics import stochasticpy

_concentrations_lookup = {
        'FixedConcentration': ['concentration'],
        'FixedReagent': ['initial_concentration',
            'filament_tip_concentration', 'number_of_filaments'] }

_end_conditions_lookup = {
        'Duration': ['duration'],
        'EventCount': ['max_events'] }

_filaments_lookup = {
        'SegmentedFilament': ['seed_concentration',
            'filament_tip_concentration', 'state'],
        'DefaultFilament': ['seed_concentration',
            'filament_tip_concentration', 'state'] }

_measurements_lookup = {
        'FilamentLength': ['sample_period'],
        'StateCount': ['state', 'sample_period'] }

_transitions_lookup = {
        'CooperativeHydrolysis': ['pointed_neighbor', 'old_state',
            'new_state', 'rate', 'cooperativity'],
        'CooperativeHydrolysisWithByproduct': ['pointed_neighbor', 'old_state',
            'new_state', 'rate', 'byproduct', 'cooperativity'],
        'BarbedEndDepolymerization': ['state', 'rate', 'disable_time'],
        'PointedEndDepolymerization': ['state', 'rate', 'disable_time'],
        'BarbedEndPolymerization': ['state', 'rate', 'disable_time'],
        'PointedEndPolymerization': ['state', 'rate', 'disable_time'],
        'RandomHydrolysis': ['old_state', 'new_state',
            'rate', 'cooperativity'],
        'RandomHydrolysisWithByproduct': ['old_state', 'new_state',
            'rate', 'byproduct'],
        'VectorialHydrolysis': ['pointed_neighbor', 'old_state',
            'new_state', 'rate'],
        'VectorialHydrolysisWithByproduct': ['pointed_neighbor', 'old_state',
            'new_state', 'rate', 'byproduct'] }

def build_binding(binding, parameters, module, lookup):
    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in bind.variable_arguments.iteritems())

    kwargs = dict(var_args)
    kwargs['label'] = binding.label
    kwargs.update(binding.fixed_arguments)
    # maybe?
#    kwargs.update(parameters)

    argument_names = lookup[class_name]
    arguments = [kwargs.get(an) for an in argument_names
            if kwargs.get(an) is not None]

    return getattr(module, binding.class_name)(*arguments)

def make_bindings(bindings, parameters, module, lookup):
    results = []
    for binding in bindings:
        results.append(build_binding(binding, parameters,
            module, lookup))
    return results


def bind_concentrations(bindings, parameters):
    states = [b.label for b in bindings]

    object_list = bind_bindings(bindings, parameters,
            stochasticpy.concentrations, _concentrations_lookup)
    return dict(zip(states, object_list))

def bind_end_conditions(bindings, parameters):
    return bind_bindings(bindings, parameters,
            stochasticpy.end_conditions, _end_conditions_lookup)

def bind_filaments(bindings, parameters):
    filaments = []
    for i in xrange(parameters['number_of_filaments']):
        filaments.append(build_binding(bindings[0], parameters,
            stochasticpy.filaments, _filaments_lookup))
    return filaments

def bind_measurements(bindings, parameters):
    return bind_bindings(bindings, parameters,
            stochasticpy.measurements, _measurements_lookup)

def bind_transitions(bindings, parameters):
    return bind_bindings(bindings, parameters,
            stochasticpy.transitions, _transitions_lookup)


def build_dict(definition, parameters, module, lookup):
    class_name = definition['class_name']
    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in
              definition.get('variable_arguments', {}).iteritems())

    kwargs = dict(var_args)
    kwargs.update(definition.get('fixed_arguments', {}))

    argument_names = lookup[class_name]
    arguments = [kwargs.get(an) for an in argument_names
            if kwargs.get(an) is not None]

    result = getattr(module, class_name)(*arguments)
    print result
    return result

def make_dicts(definitions, parameters, module, lookup):
    return [build_dict(d, parameters, module, lookup)
            for d in definitions]

def dict_concentrations(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())

    object_list = make_dicts(definitions, parameters,
            stochasticpy.concentrations, _concentrations_lookup)
    result = stochasticpy.ConcentrationContainer()
    for l, o in zip(labels, object_list):
        result[l] = o
    return result

def dict_end_conditions(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())
    result = stochasticpy.EndConditionContainer()
    for item in make_dicts(definitions, parameters,
            stochasticpy.end_conditions, _end_conditions_lookup):
        result.append(item)
    return result

def dict_filaments(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())
    filaments = stochasticpy.FilamentContainer()
    for i in xrange(parameters['number_of_filaments']):
        f = build_dict(definitions[0], parameters,
                stochasticpy.filaments, _filaments_lookup)
        filaments.append(f)
    return filaments

def dict_measurements(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())
    result = stochasticpy.MeasurementContainer()
    for item in make_dicts(definitions, parameters,
            stochasticpy.measurements, _measurements_lookup):
        result.append(item)
    return result

def dict_transitions(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())
    result = stochasticpy.TransitionContainer()
    for item in make_dicts(definitions, parameters,
            stochasticpy.transitions, _transitions_lookup):
        result.append(item)
    return result
