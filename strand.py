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

from numpy.random import mtrand
import copy

class Strand(object):
    """
    Single ended strand for studying filament tip dynamics.
    This object is meant to have an interface much like a normal python list,
    despite different interal structure and some extra goodies.
    """
    def __init__(self, tailsize, tailstate):
        self._substrands = [ (tailsize, tailstate) ]

    # Addition and removal operators
    def append(self, state):
        """
        Adds an element in the given state to the tail end of the strand.
        """
        end = self._substrands[-1]
        if end[1] == state:
            self._substrands[-1] = ( end[0] + 1, state )
        else:
            self._substrands.append( (1, state) )
    def pop(self):
        """
        Returns and removes one element from the end of the strand.
        """
        end = self._substrands[-1]
        st = end[1]
        if 1 == end[0]:
            del self._substrands[-1]
        else:
            self._substrands[-1] = (end[0] - 1, st)
        if not self._substrands:
            print "holy shit batman, we emptied the reservior."
            raise self
        return st

    # Misc list operators
    def reverse(self):
        self._substrands.reverse()

    # Accessors
    def peek(self):
        """
        Returns the state of the end of the strand.
        """
        return self._substrands[-1][1]
#    def __getitem__(self, i):
#        return i

    def __len__(self):
        num = 0
        for sub in self._substrands:
            num += sub[0]
        return num

    # Statistical/measurement operators
    def count(self, state):
        """
        Returns the number of elements matching state.
        """
        num = 0
        for sub in self._substrands:
            if sub[1] == state:
                num += sub[0]
        return num

    def count_not(self, state):
        """
        Returns the number of elements not matching state.

        For example to find the cap length, you might use:
            cap_length = strand.count_not( ChemicalState.ADP )
        """
        num = 0
        for sub in self._substrands:
            if sub[1] != state:
                num += sub[0]
        return num
    def sanity_check(self):
        for s in self._substrands:
            assert( 0 < s[0] )

    # Evolution operators
    def evolve(self, probabilities):
        """
        Evolves the strand by one step.  Essentially used for hydrolization and
        other changes of state that monomers in the filament might go through.

        This will not add or remove monomers, only change their states.

        The probabilities dictionary must have the following form:
            probabilities[ ExampleState ] -> [ (0.050, State1),
                                               (0.211, State2),
                                               (0.533, State3),
                                               (0.706, State4) ]
        The list returned by probabilities must be sorted in increasing order.
        Each element in the strand will be allowed to evolve into one state.
        If the random number generated is more than any of the numbers,
        the state will not change.  If it is less than  any of the nubers,
        it will be changed into the first state it is less than.
        """
        new_substrands = []
        for substrand in self._substrands:
            new_substrands = _join_strands( new_substrands,
                    _evolve_substrand(substrand, probabilities[substrand[1]]) )
        self._substrands = new_substrands

# Helper functions
def _join_strands(left, right):
    if not left:
        return right
    if not right:
        return left
    left_end    = left[-1]
    right_begin = right[0]
    lc = copy.copy(left)
    if left_end[1] == right_begin[1]:
        lc[-1] = (left_end[0] + right_begin[0], left_end[1])
        lc.extend( right[1:] )
    else:
        lc.extend( right )
    return lc

def _evolve_substrand(substrand, probs):
    if not probs:
        return [substrand]
    rnums = mtrand.rand( substrand[0] )
    states = map( lambda x: _choose_state( probs, x, substrand[1] ), rnums )

    result_strand = []
    current_count = None
    current_state = None
    for s in states:
        if not current_state:
            current_state = s
            current_count = 1
        elif s == current_state:
            current_count += 1
        else:
            result_strand.append( (current_count, current_state) )
            current_state = s
            current_count = 1
    result_strand.append( (current_count, current_state) )
    return result_strand

def _choose_state( probs, num, default=None ):
    for rate, state in probs:
        if num < rate:
            return state
    return default
