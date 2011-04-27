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

import yaml
import os.path
import sys

from .. import logger
log = logger.getLogger(__file__)

def load_definition(filename, source_directory=None):
    definition = _read_definition(filename)
    return _expand_imports(definition, source_directory=source_directory)


def validate_definition(definition):
    valid_structure  = _validate_structure(definition)
    valid_bindings   = _validate_bindings(definition)
    valid_parameters = _validate_parameters(definition)

    log.debug('Input file validation: structure=%s, bindings=%s, parameters=%s',
            valid_structure, valid_bindings, valid_parameters)

    return valid_structure and valid_bindings and valid_parameters


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


def _validate_structure(definition):
    '''
    Validate overall structure.
    '''
    return False


def _validate_bindings(definition):
    '''
    Validate binding class names.
    '''
    return False


def _validate_parameters(definition):
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
        log.debug('Extra parameter names: %s', extra_parameter_names)

    if missing_parameter_names:
        log.error('Missing parameters: %s', missing_parameter_names)
        return False
    return True

def _search_variable_arguments(definition, result_set):
    var_args = definition.get('variable_arguments', {})
    for name in var_args.values():
        result_set.add(name)

    for name, child in definition.iteritems():
        if isinstance(child, dict):
            _search_variable_arguments(child, result_set)
        elif isinstance(child, list):
            for element in child:
                _search_variable_arguments(element, result_set)
