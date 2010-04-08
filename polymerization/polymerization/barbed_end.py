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
    def __init__(self, rate, state):
        self.rate  = rate
        self.state = state
        self.R     = rate
    
    def initialize(self, strand):
        self.strand = strand

    def perform(self, r):
        self.strand.append(self.state)
        return ('poly', 'barbed')

    def update(self, transition_output):
        pass
