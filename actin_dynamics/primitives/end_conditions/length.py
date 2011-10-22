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

from base_classes import EndCondition as _EndCondition

class MinLength(_EndCondition):
    'End simulation after duration seconds.'

    __slots__ = ['duration']
    def __init__(self, value=None, label=None):
        self.value = value
        _EndCondition.__init__(self, label=label)

    def reset(self):
        pass

    def __call__(self, time, filaments, concentrations):
        for f in filaments:
            if len(f) < self.value:
                return True
        return False
