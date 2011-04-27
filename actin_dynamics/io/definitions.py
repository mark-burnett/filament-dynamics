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
    definition = read_definition(filename)
    return expand_imports(definition, source_directory=source_directory)


def read_definition(filename):
    results = None
    log.debug("Loading definition from '%s'.", filename)
    try:
        with open(filename) as f:
            results = yaml.load(f)
    except IOError:
        log.critical("Definition file '%s' not loaded.", filename)
        raise

    return results

def expand_imports(data, source_directory=None):
    '''
    Recursively search and expand import statements in input files.
    '''
    # Top level
    import_filenames = data.pop('import', [])
    for import_filename in import_filenames:
        try:
            local_definition = read_definition(os.path.join(source_directory,
                import_filename))
        except IOError:
            log.critical('Failure importing from file %s.', from_file)
            raise

        data = merge_dicts(data, local_definition)

    # Immediate Children
    for name, child in data.iteritems():
        if isinstance(child, dict):
            data[name] = expand_imports(child,
                    source_directory=source_directory)
        elif isinstance(child, list):
            for i, element in enumerate(child):
                child[i] = expand_imports(element,
                        source_directory=source_directory)

    return data

def merge_dicts(a, b):
    keys = set(a.keys()).union(set(b.keys()))

    result = {}
    for key in keys:
        if key != 'import':
            if key not in a:
                result[key] = b[key]
            elif key not in b:
                result[key] = a[key]
            else: # key in both
                result[key] = merge_dicts(a[key], b[key])

    return result

def validate_definition(definition):
    return False
