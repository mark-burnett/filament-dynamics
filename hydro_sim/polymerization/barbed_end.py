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

__all__ = ['FixedRate']

class FixedRate(object):
    __slots__ = ['rate', 'strand', 'state', 'R']
    def __init__(self, rate, state):
        """
            'rate' is the number per second of 'state' that are added to the
        barbed end of the strand.
        """
        self.rate  = rate
        self.state = state
        self.R     = rate
    
    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        self.strand.append(self.state)
        return ('poly', ('barbed', self.state))

    def update(self, transition_output):
        pass

class FixedReagent(object):
    __slots__ = ['rate', 'strand', 'amount', 'state', 'R']
    def __init__(self, rate_per_unit, amount, state):
        """
            'rate_per_unit' * 'amount' is the number of 'state' that are added
        per second to the barbed end of the strand.
        """
        self.rate = rate_per_unit
        self.amount = amount
        self.state = state
        assert(self.amount >= 0)
    
    def initialize(self, strand):
        self.strand = strand
        self.R = self.rate * self.amount

    def perform(self, r):
        assert(self.amount > 0)
        self.strand.append(self.state)
        self.amount -= 1
        self.R = self.rate * self.amount
        return ('poly', ('barbed', self.state))

    def update(self, transition_output):
        command, value = transition_output
        if 'depoly' == command:
            end, state = value
            if self.state == state:
                self.amount += 1
                self.R = self.rate * self.amount
