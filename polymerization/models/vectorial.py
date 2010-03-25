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

import random

from compact_strand import CompactStrand
from compact_strand import cleanup_substrands

from polymerization.rates.util import choose_state

__all__ = ['hydrolysis', 'strand']

class Hydrolysis(object):
    """
    Hydrolysis object for a vectorial hydrolysis model.
    """
    def __init__(self, rates):
        self.rates = rates

    def __call__(self, strand, hstats):
        new_substrands = []

        for s in strand.substrands:
            new_state = choose_state(self.rates[s[1]], random.random())
            if new_state:
                # Add the new element
                new_substrands.append((1, new_state))
                # Add the rest of this substrand
                if s[0] > 1:
                    new_substrands.append((s[0]-1, s[1]))
            else:
                new_substrands.append(s)
        strand.substrands = cleanup_substrands(new_substrands)

# Lowercase alias
hydrolysis = Hydrolysis

def strand(initial_sequence=None, initial_state=None, initial_length=None,
        barbed_end=True, pointed_end=True):
    if initial_sequence:
        result = CompactStrand(0, None)
        result.substrands = cleanup_substrands(
                                [(1, x) for x in initial_sequence])
        return result

    return CompactStrand(initial_length, initial_state)
