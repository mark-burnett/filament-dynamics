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

from base_classes import Transition as _Transition

class _FixedRate(_Transition):
    skip_registration = True
    parameters = ['rate']
    states = ['state']

    __slots__ = ['state', 'rate']
    def __init__(self, state, rate):
        """
        state - state to depolymerize
        rate  - depolymerization rate (constant)
        """
        self.state = state
        self.rate  = rate
        _Transition.__init__(self)

    def R(self, strand, concentrations):
        if self.state == strand[-1]:
            return self.rate
        return 0

    def perform(self, time, strand, concentrations, r):
        _Transition.perform(self, time, strand, concentrations, r)

class BarbedDepolymerization(_FixedRate):
    def perform(self, time, strand, concentrations, r):
        strand.shrink_barbed_end()
        concentrations[self.state].add_monomer()
        _FixedRate.perform(self, time, strand, concentrations, r)
