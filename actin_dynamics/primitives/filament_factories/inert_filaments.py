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

from base_classes import FilamentFactory as _FilamentFactory

from actin_dynamics.state.single_strand_filaments import Filament

class InertFilament(_FilamentFactory):
    def __init__(self, state=None, label=None):
        self.state = state
        _FilamentFactory.__init__(self, label=label)

    def create(self):
        return [Filament([state]) for i in xrange(self.number)]
