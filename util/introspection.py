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

def lookup_name(name, module):
    m = module
    for n in name.split('.'):
        m = m.__getattribute__(n)
    return m

def make_factories(config_list, module):
    return [(lookup_name(name, module), args)
            for name, args in config_list]

def make_kwargs_ascii(kwargs):
    return dict((str(k), v) for k, v in kwargs.iteritems())
