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

from hydro_sim.transitions import events

__all__ = ['Barbed', 'Pointed']

class GeneralFixedRate(object):
    __slots__ = ['pub', 'state', 'rate', 'strand']
    def __init__(self, pub, concentrations, state, rate):
        """
        pub - publisher for transition events.
        concentrations - unused, but required for consistent interface
        state - state to depolymerize
        rate - depolymerization rate (constant)
        """
        self.pub   = pub
        self.state = state
        self.rate  = rate

    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        raise NotImplementedError()

class Barbed(GeneralFixedRate):
    def perform(self, r, time):
        self.pub.publish(events.depolymerization('barbed', self.strand.pop(),
                                                 time))

    @property
    def R(self):
        if self.state == self.strand[-1]:
            return self.rate
        else:
            return 0

class Pointed(GeneralFixedRate):
    def perform(self, r, time):
        self.pub.publish(events.depolymerization('pointed',
                                                 self.strand.popleft(), time))

    @property
    def R(self):
        if self.state == self.strand[0]:
            return self.rate
        else:
            return 0
