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

from base_classes import Transition as _FilamentTransition

class _FixedRate(_FilamentTransition):
    skip_registration = True
    __slots__ = ['rate', 'state']
    def __init__(self, state=None, rate=None):
        """
        'state' that are added to the barbed end of the strand.
        'rate' is the number per second per concentration of
        """
        self.state = state
        self.rate  = rate

        _FilamentTransition.__init__(self)

    def R(self, filaments, concentrations):
        return [self.rate * concentrations[self.state].value
                for s in filaments]

    def perform(self, time, filaments, concentrations, index, r):
        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)


class BarbedPolymerization(_FixedRate):
    'Simple polymerization at the barbed end.'
    def perform(self, time, filaments, concentrations, index, r):
        current_strand = filaments[index]
        current_strand.grow_barbed_end(self.state)
        concentrations[self.state].remove_monomer()
        _FixedRate.perform(self, time, filaments, concentrations, index, r)
