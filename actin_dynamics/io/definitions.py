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
    if not source_directory:
        source_directory, partial_filename = _backward_path_split(filename)
#        source_directory, partial_filename = os.path.split(filename)
        full_filename = filename
    else:
        full_filename = os.path.join(source_directory, filename)

    results = None
    log.debug("Loading definition from '%s'.", filename)
    try:
        with open(full_filename) as f:
            results = yaml.load(f)
    except IOError:
        log.exception("Definition file '%s' not loaded.", full_filename)
        sys.exit()

    imports = results.get('import', [])
    for import_filename in imports:
        try:
            results = merge_dicts(results, load_definition(
                import_filename, source_directory=source_directory))
        except IOError:
            raise
        except Exception as e:
            log.exception("Failed to load '%s' from '%s'.",
                    import_filename, source_directory)
            raise IOError(e)

    return results


def _backward_path_split(filename):
    left, right = os.path.split(filename)
    left_result = left
    right_result = right

    while left:
        left, right = os.path.split(left)
        if left:
            left_result = left
            right_result = os.path.join(right, right_result)

    return left_result, right_result


def merge_dicts(a, b):
    try:
        keys = set(a.keys()).union(set(b.keys()))
    except AttributeError:
        log.exception('Error merging input files.  Perhaps you have duplicated a parameter entry?')
        raise

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
