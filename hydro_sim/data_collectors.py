#    Copyright (C) 2009 Mark Burnett
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

import copy

def strand_length(kwargs):
    return len(kwargs['strand'])

class Variable(object):
    __slots__ = ['var_name']
    def __init__(self, var_name):
        self.var_name = var_name
    def __call__(self, kwargs):
        return kwargs[self.var_name]

class HydrolysisEventCounter(object):
    __slots__ = ['old_states', 'new_states', 'count']
    def __init__(self, old_states, new_states):
        try:
            iter(old_states)
            self.old_states = old_states
        except TypeError:
            self.old_states = [old_states]

        try:
            iter(new_states)
            self.new_states = new_states
        except TypeError:
            self.new_states = [new_states]

        self.count = 0

    def __call__(self, kwargs):
        transition, value = kwargs['transition_output']
        if 'hydrolysis' == transition:
            (old, new), i = value
            if old in self.old_states and new in self.new_states:
                self.count += 1
        return self.count

def count_not(neg_state, kwargs):
    """
    Counts the number of monomers in the strand not in 'state'.
    """
    s = kwargs['strand']
    return len(s) - s.count(neg_state)

def count(state, kwargs):
    """
    Counts the number of monomers in the strand in 'state'.
    """
    return kwargs['strand'].count(state)

def tip_state(kwargs):
    """
    Peeks at the tip state of the strand.
    """
    return kwargs['strand'][-1]
 
# More intensive measurements.
def copy_strand(kwargs):
    """
    Makes a copy of the entire strand.
    """
    return copy.copy(kwargs['strand'])
