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

def get_flags(flag_text, prefix='', postfix='', module=None):
    flags = 0
    for attr in _force_iterable(flag_text):
        flags = flags | getattr(module, prefix + attr.upper() + postfix, 0)
    return flags

def _force_iterable(item):
    if isinstance(item, basestring):
        return [item]

    try:
        i = iter(item)
    except TypeError:
        i = [item]
    return i
