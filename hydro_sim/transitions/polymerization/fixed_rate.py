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
    __slots__ = ['pub', 'rate', 'state', 'R', 'concentration', 'strand']
    def __init__(self, pub, concentrations, state, rate):
        """
        'pub' is a publisher object,
        'concentrations' is a dictionary of the state concentration callables
        'rate' is the number per second per concentration of
        'state' that are added to the barbed end of the strand.
        """
        self.concentration = concentrations[state]

        self.pub   = pub
        self.rate  = rate
        self.state = state
        self.R     = rate * self.concentration()

        # Subscribe to polymerization and depolymerization events.
        self.pub.subscribe(self.update, events.polymerization)
        self.pub.subscribe(self.update, events.depolymerization)
    
    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        raise NotImplementedError()

    def update(self, event):
        if self.state == event.state:
            self.R = self.rate * self.concentration()

class Barbed(GeneralFixedRate):
    def perform(self, r, time):
        self.strand.append(self.state)
        self.pub.publish(events.polymerization('barbed', self.state, time))

class Pointed(GeneralFixedRate):
    def perform(self, r, time):
        self.strand.appendleft(self.state)
        self.pub.publish(events.polymerization('pointed', self.state, time))
