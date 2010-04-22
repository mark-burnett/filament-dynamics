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

from transitions import events

__all__ = ['FixedRate']

class FixedRate(object):
    def __init__(self, pub, state, rate):
        self.pub   = pub
        self.state = state
        self.rate  = rate

    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        pub.publish(events.depolymerization('barbed', self.strand.pop()))

    @property
    def R(self):
        if state == self.strand[-1]:
            return self.rate
        else:
            return 0
