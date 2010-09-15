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

from base_classes import SolutionTransition as _SolutionTransition
from . import mixins as _mixins

class ConcentrationChange(_SolutionTransition):
    parameters = ['rate']
    states = ['old_state', 'new_state']

    __slots__ = ['old_state', 'rate', 'new_state']
    def __init__(self, old_state=None, rate=None, new_state=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state

        _SolutionTransition.__init__(self)

    def R(self, strands, concentrations):
        return self.rate * concentrations[self.old_state].value

    def perform(self, time, strands, concentrations, index, r):
        concentrations[self.old_state].remove_monomer()
        concentrations[self.new_state].add_monomer()

        _SolutionTransition.perform(self, time, strands, concentrations, index, r)


ConcentrationChangeWithByproduct = _mixins.add_byproduct(ConcentrationChange)
