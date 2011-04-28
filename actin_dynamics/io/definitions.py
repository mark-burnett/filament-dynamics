#    Copyright (C) 2011 Mark Burnett
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

import pprint
import collections
import yaml
import os.path
import sys

from actin_dynamics import primitives

from .. import logger
log = logger.getLogger(__file__)

def load_definition(filename, source_directory=None):
    definition = _read_definition(filename)
    return _expand_imports(definition, source_directory=source_directory)


def validate_definition(definition, verbose=False):
    valid_bindings   = _validate_bindings(definition, verbose=verbose)
    valid_parameters = _validate_parameters(definition, verbose=verbose)

    log.debug('Input file validation: bindings=%s, parameters=%s',
            valid_bindings, valid_parameters)

    return valid_bindings and valid_parameters


def _read_definition(filename):
    results = None
    log.debug("Loading definition from '%s'.", filename)
    try:
        with open(filename) as f:
            results = yaml.load(f)
    except IOError:
        log.critical("Definition file '%s' not loaded.", filename)
        raise

    return results

def _expand_imports(data, source_directory=None):
    '''
    Recursively search and expand import statements in input files.
    '''
    # Top level
    import_filenames = data.pop('import', [])
    for import_filename in import_filenames:
        try:
            local_definition = _read_definition(os.path.join(source_directory,
                import_filename))
        except IOError:
            log.critical('Failure importing from file %s.', from_file)
            raise

        data = _merge_dicts(data, local_definition)

    # Immediate Children
    for name, child in data.iteritems():
        if isinstance(child, dict):
            data[name] = _expand_imports(child,
                    source_directory=source_directory)
        elif isinstance(child, list):
            for i, element in enumerate(child):
                child[i] = _expand_imports(element,
                        source_directory=source_directory)

    return data

def _merge_dicts(a, b):
    keys = set(a.keys()).union(set(b.keys()))

    result = {}
    for key in keys:
        if key != 'import':
            if key not in a:
                result[key] = b[key]
            elif key not in b:
                result[key] = a[key]
            else: # key in both
                result[key] = _merge_dicts(a[key], b[key])

    return result


def _validate_bindings(definition, verbose=False):
    '''
    Validate binding class names.
    '''
    missing_class_names = collections.defaultdict(set)

    stage_components = ['transitions', 'concentrations',
                        'end_conditions', 'observers']

    missing_mt = _check_definition(definition.get('model_transitions', {}),
                                                  module_name='transitions')
    if missing_mt:
        map(missing_class_names['transitions'].add, missing_mt)

    missing_pars = _check_definition(definition.get('variable_parameters', {}),
                                     module_name='parameters')
    if missing_pars:
        map(missing_class_names['parameters'].add, missing_pars)

    for expt_name, experiment in definition.get('experiments', {}).iteritems():
        # filament factory
        # XXX restructure primitives directory to match
        class_name = experiment.get('filament_factory', {}
                ).get('class_name', None)
        if class_name not in primitives.filament_factories.registry:
            missing_class_names['filament_factories'].add(class_name)

        # Stage
        for stage in experiment.get('stages', []):
            for sc in stage_components:
                missing_sc = _check_definition(stage.get(sc, {}),
                                               module_name=sc)
                if missing_sc:
                    map(missing_class_names[sc].add, missing_sc)

        # analysts
        # XXX restructure primitives directory to match
        for a in experiment.get('analysts', []):
            class_name = a.get('class_name', None)
            if class_name not in primitives.analysts.registry:
                missing_class_names['analysts'].add(class_name)

        fitting = experiment.get('fitting', {})

        # fitting
            # discriminators
            # data loaders

        missing_data = _check_definition(fitting.get('data', {}),
                module_name='file_readers')
        if missing_data:
            map(missing_class_names['file_readers'].add, missing_data)

        # XXX restructure primitives directory to match
        missing_discriminators = _check_definition(
                fitting.get('discriminators', {}),
                module_name='discriminators')
        if missing_discriminators:
            map(missing_class_names['discriminators'].add,
                missing_discriminators)


    if missing_class_names:
        if verbose:
            print 'Missing primitive definitions:'
            pprint.pprint(dict(missing_class_names))
        log.error('Missing primitives: %s', dict(missing_class_names))
        return False

    return True

def _check_definition(definition, module_name=None):
    if not definition:
        return []
    registry = getattr(primitives, module_name).registry
    result = []
    for label, t in definition.iteritems():
        class_name = t.get('class_name', None)
        if class_name not in registry:
            result.append(class_name)
    return result

def _validate_parameters(definition, verbose=False):
    '''
    Make sure we can find every parameter we use.
    '''
    expected_parameter_names = set()
    _search_variable_arguments(definition, expected_parameter_names)

    available_parameter_names = set(
            definition.get('fixed_parameters', {}).keys() +
            definition.get('variable_parameters', {}).keys())
    missing_parameter_names = expected_parameter_names - available_parameter_names

    extra_parameter_names = available_parameter_names - expected_parameter_names
    if extra_parameter_names:
        if verbose:
            print 'Unused parameters:'
            pprint.pprint(extra_parameter_names)
        log.debug('Extra parameter names: %s', extra_parameter_names)

    if missing_parameter_names:
        if verbose:
            print 'Missing parameters:'
            pprint.pprint(missing_parameter_names)
        log.error('Missing parameters: %s', missing_parameter_names)
        return False

    return True

def _search_variable_arguments(definition, result_set):
    var_args = definition.get('variable_arguments', {})
    for name in var_args.values():
        result_set.add(name)

    sample_period = definition.get('sample_period', None)
    if sample_period:
        result_set.add(sample_period)
    number_of_simulations = definition.get('number_of_simulations', None)
    if number_of_simulations:
        result_set.add(number_of_simulations)

    for name, child in definition.iteritems():
        if isinstance(child, dict):
            _search_variable_arguments(child, result_set)
        elif isinstance(child, list):
            for element in child:
                _search_variable_arguments(element, result_set)
