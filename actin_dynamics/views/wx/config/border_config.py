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

class wxBorderConfig(object):
    def __init__(self, border_definitions):
        self.border_definitions = border_definitions

    def __call__(self, name):
        return self.border_definitions[name]

    @classmethod
    def from_configobj(cls, config):
        border_definitions = {}
        for name, value in config.iteritems():
            border_definitions[name] = int(value)

        return cls(border_definitions)
