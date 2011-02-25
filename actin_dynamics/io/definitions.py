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

def load_definition(filename, source_directory='configuration'):
    results = None
    with open(os.path.join(source_directory, filename)) as f:
        results = yaml.load(f)

    imports = results.get('import', [])
    for import_filename in imports:
        results = merge_dicts(results,
                load_session_definition(import_filename, source_directory))

    return results

def merge_dicts(a, b):
    keys = set(a.keys()).union(set(b.keys()))

    result = {}
    for key in keys:
        if key not in a:
            result[key] = b[key]
        elif key not in b:
            result[key] = a[key]
        else: # key in both
            result[key] = _merge_dicts(a[key], b[key])

    return result