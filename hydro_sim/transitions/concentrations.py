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

class FixedRate(object):
    __slots__ = ['old_state', 'rate', 'new_state']
    def __init__(self, old_state, rate, new_state):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state
    
    def R(self, strand):
        return self.rate * strand.concentrations[self.old_state]

    def perform(self, time, strand, r):
        strand.concentrations[self.old_state].remove_monomer()
        strand.concentrations[self.new_state].add_monomer()
