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

from actin_dynamics import logger as _logger
log = _logger.getLogger(__file__)

_concentrations_lookup = {
        'FixedConcentration': [
            (float, 'concentration', None)],
        'FixedReagent': [
            (float, 'initial_concentration', None),
            (float, 'filament_tip_concentration', None),
            (int, 'number_of_filaments', None),
            (float, 'scale_concentration', 1),
            (float, 'subtract_fraction', 0)] }

_end_conditions_lookup = {
        'Duration': [
            (float, 'duration', None)],
        'EventCount': [
            (int, 'max_events', None)],
        'Threshold': [
            (str, 'concentration_name', None),
            (float, 'value', None),
            (float, 'scaled_by', 1),
            (float, 'subtract_fraction', 0)] }

_filaments_lookup = {
        'SegmentedFilament': [
            (float, 'seed_concentration', None),
            (float, 'filament_tip_concentration', None),
            (str, 'state', None)],
        'DefaultFilament': [
            (float, 'seed_concentration', None),
            (float, 'filament_tip_concentration', None),
            (str, 'state', None)] }

_measurements_lookup = {
        'BarrierPosition': [
            (float, 'sample_period', None)],
        'BarrierForce': [
            (float, 'sample_period', None),
            (int, 'divisions', None),
            (int, 'rest_position', None),
            (float, 'spring_constant', None)],
        'Concentration': [
            (str, 'state', None),
            (float, 'sample_period', None)],
        'FilamentLength': [
            (float, 'sample_period', None)],
        'TipStateMatches': [
            (str, 'state', None),
            (float, 'sample_period', None),
            (int, 'number_of_filaments', None)],
        'StateCount': [
            (str, 'state', None),
            (float, 'sample_period', None)] }

_transitions_lookup = {
        'Association': [
            (str, 'associating_state', None),
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None)],
        'CooperativeHydrolysis': [
            (str, 'pointed_neighbor', None),
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (float, 'cooperativity', None)],
        'CooperativeHydrolysisWithByproduct': [
            (str, 'pointed_neighbor', None),
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None),
            (float, 'cooperativity', None)],
        'BarbedEndDepolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (float, 'disable_time', -1)],
        'PointedEndDepolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (float, 'disable_time', -1)],
        'Monomer': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None)],
        'MonomerWithByproduct': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None)],
        'BarbedEndPolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (float, 'disable_time', -1)],
        'PointedEndPolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (float, 'disable_time', -1)],
        'RandomHydrolysis': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (float, 'cooperativity', None)],
        'RandomHydrolysisWithByproduct': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None)],
        'BarbedTipHydrolysis': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None)],
        'PointedTipHydrolysis': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None)],
        'BarbedTipHydrolysisWithByproduct': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None)],
        'PointedTipHydrolysisWithByproduct': [
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None)],
        'VectorialHydrolysis': [
            (str, 'pointed_neighbor', None),
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None)],
        'VectorialHydrolysisWithByproduct': [
            (str, 'pointed_neighbor', None),
            (str, 'old_state', None),
            (str, 'new_state', None),
            (float, 'rate', None),
            (str, 'byproduct', None)],
        'RaiseBarrierConstantForce': [
            (float, 'force', None),
            (float, 'D', None),
            (int, 'divisions', 1)],
        'LowerBarrierConstantForce': [
            (float, 'force', None),
            (float, 'D', None),
            (int, 'divisions', 1)],
        'RaiseBarrierSpringForce': [
            (float, 'spring_constant', None),
            (int, 'rest_position', None),
            (float, 'D', None),
            (int, 'divisions', 1)],
        'LowerBarrierSpringForce': [
            (float, 'spring_constant', None),
            (int, 'rest_position', None),
            (float, 'D', None),
            (int, 'divisions', 1)],
        'StepFunctionBarrierBarbedEndPolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (int, 'divisions', 1)],
        'LinearFunctionBarrierBarbedEndPolymerization': [
            (str, 'state', None),
            (float, 'rate', None),
            (int, 'divisions', 1),
            (int, 'linear_width', 1)]
        }

def build_binding(binding, parameters, module, lookup):
    class_name = binding.class_name
    var_args = dict((local_name, parameters[global_name])
          for local_name, global_name in
              binding.variable_arguments.iteritems())

    kwargs = dict(var_args)
    kwargs['label'] = binding.label
    kwargs.update(binding.fixed_arguments)

    argument_names = lookup[class_name]
    arguments = [ctor(kwargs.get(an, default_value))
                    for ctor, an, default_value in argument_names
            if kwargs.get(an, default_value) is not None]

    log.debug('module = %s, class name = %s', module, class_name)
    log.debug('args = %s', arguments)

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
    arguments = [ctor(kwargs.get(an, default_value))
                    for ctor, an, default_value in argument_names
            if kwargs.get(an, default_value) is not None]

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
