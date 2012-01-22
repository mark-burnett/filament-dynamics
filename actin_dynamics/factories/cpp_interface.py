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
        'FixedConcentration': [
            (float, 'concentration')],
        'FixedReagent': [
            (float, 'initial_concentration'),
            (float, 'filament_tip_concentration'),
            (int, 'number_of_filaments')] }

_end_conditions_lookup = {
        'Duration': [
            (float, 'duration')],
        'EventCount': [
            (int, 'max_events')] }

_filaments_lookup = {
        'SegmentedFilament': [
            (float, 'seed_concentration'),
            (float, 'filament_tip_concentration'),
            (str, 'state')],
        'DefaultFilament': [
            (float, 'seed_concentration'),
            (float, 'filament_tip_concentration'),
            (str, 'state')] }

_measurements_lookup = {
        'Concentration': [
            (str, 'state'),
            (float, 'sample_period')],
        'FilamentLength': [
            (float, 'sample_period')],
        'StateCount': [
            (str, 'state'),
            (float, 'sample_period')] }

_transitions_lookup = {
        'Association': [
            (str, 'associating_state'),
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate')],
        'CooperativeHydrolysis': [
            (str, 'pointed_neighbor'),
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (float, 'cooperativity')],
        'CooperativeHydrolysisWithByproduct': [
            (str, 'pointed_neighbor'),
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct'),
            (float, 'cooperativity')],
        'BarbedEndDepolymerization': [
            (str, 'state'),
            (float, 'rate'),
            (float, 'disable_time')],
        'PointedEndDepolymerization': [
            (str, 'state'),
            (float, 'rate'),
            (float, 'disable_time')],
        'Monomer': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate')],
        'MonomerWithByproduct': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct')],
        'BarbedEndPolymerization': [
            (str, 'state'),
            (float, 'rate'),
            (float, 'disable_time')],
        'PointedEndPolymerization': [
            (str, 'state'),
            (float, 'rate'),
            (float, 'disable_time')],
        'RandomHydrolysis': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (float, 'cooperativity')],
        'RandomHydrolysisWithByproduct': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct')],
        'BarbedTipHydrolysis': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate')],
        'PointedTipHydrolysis': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate')],
        'BarbedTipHydrolysisWithByproduct': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct')],
        'PointedTipHydrolysisWithByproduct': [
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct')],
        'VectorialHydrolysis': [
            (str, 'pointed_neighbor'),
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate')],
        'VectorialHydrolysisWithByproduct': [
            (str, 'pointed_neighbor'),
            (str, 'old_state'),
            (str, 'new_state'),
            (float, 'rate'),
            (str, 'byproduct')] }

def build_binding(binding, parameters, module, lookup):
    class_name = binding.class_name
    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in
              binding.variable_arguments.iteritems())

    kwargs = dict(var_args)
    kwargs['label'] = binding.label
    kwargs.update(binding.fixed_arguments)

    argument_names = lookup[class_name]
    arguments = [ctor(kwargs.get(an)) for ctor, an in argument_names
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

    result = stochasticpy.ConcentrationContainer()
    object_list = make_bindings(bindings, parameters,
            stochasticpy.concentrations, _concentrations_lookup)
    for s, o in zip(states, object_list):
        result[s] = o
    return result

def bind_end_conditions(bindings, parameters):
    result = stochasticpy.EndConditionContainer()
    for item in make_bindings(bindings, parameters,
            stochasticpy.end_conditions, _end_conditions_lookup):
        result.append(item)
    return result

def bind_filaments(bindings, parameters):
    filaments = stochasticpy.FilamentContainer()
    for i in xrange(int(parameters['number_of_filaments'])):
        filaments.append(build_binding(bindings[0], parameters,
            stochasticpy.filaments, _filaments_lookup))
    return filaments

def bind_measurements(bindings, parameters):
    labels = [b.label for b in bindings]
    result = stochasticpy.MeasurementContainer()
    object_list = make_bindings(bindings, parameters,
            stochasticpy.measurements, _measurements_lookup)
    for l, o in zip(labels, object_list):
        result[l] = o
    return result

def bind_transitions(bindings, parameters):
    result = stochasticpy.TransitionContainer()
    for item in make_bindings(bindings, parameters,
            stochasticpy.transitions, _transitions_lookup):
        result.append(item)
    return result


def build_dict(definition, parameters, module, lookup):
    class_name = definition['class_name']
    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in
              definition.get('variable_arguments', {}).iteritems())

    kwargs = dict(var_args)
    kwargs.update(definition.get('fixed_arguments', {}))

    argument_names = lookup[class_name]
    arguments = [ctor(kwargs.get(an)) for ctor, an in argument_names
            if kwargs.get(an) is not None]

    return getattr(module, class_name)(*arguments)

def make_dicts(definitions, parameters, module, lookup):
    return [build_dict(d, parameters, module, lookup)
            for d in definitions]

def dict_concentrations(object_graph, parameters):
    result = stochasticpy.ConcentrationContainer()
    for l, d in object_graph.iteritems():
        result[l] = build_dict(d, parameters, stochasticpy.concentrations,
                _concentrations_lookup)
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
        filaments.append(build_dict(definitions[0], parameters,
                stochasticpy.filaments, _filaments_lookup))
    return filaments

def dict_measurements(object_graph, parameters):
    result = stochasticpy.MeasurementContainer()
    for label, definition in object_graph.iteritems():
        result[label] = build_dict(definition, parameters,
                stochasticpy.measurements, _measurements_lookup)
    return result

def dict_transitions(object_graph, parameters):
    labels, definitions = zip(*object_graph.iteritems())
    result = stochasticpy.TransitionContainer()
    for item in make_dicts(definitions, parameters,
            stochasticpy.transitions, _transitions_lookup):
        result.append(item)
    return result
