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

    def __str__(self):
        return str(self._substrands)

    # Addition and removal operators
    def append(self, state):
        """
        Adds an element in the given state to the tail end of the strand.
        """
        end = self._substrands[-1]
        if end[1] == state:
            self._substrands[-1] = (end[0] + 1, state)
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

    # Evolution operators
    def hydrolysis(self, probabilities):
        """
        Performs hydrolysis on the strand given probabilities.

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
        # We need to reverse the strand to work from the barbed end.
        self.reverse()
        new_substrands = []
        last_state = None
        for substrand in self._substrands:
            num           = substrand[0]
            current_state = substrand[1]
            # Take care of the (pointed) end of the last substrand
            if last_state:
                new_substrands = _join_strands(new_substrands,
                        _substrand_transition(
                            probabilities[(last_state, current_state)],
                            last_state))
            # Deal with the bulk current substrand
            if num - 1:
                new_substrands = _join_strands(new_substrands,
                        _evolve_substrand( (num - 1, current_state),
                                 probabilities[(current_state, current_state)]))
            last_state = current_state

        # Take care of the (pointed) end of the final substrand
        new_substrands = _join_strands(new_substrands,
                _substrand_transition(
                    probabilities[(last_state, current_state)], last_state))

        changed = (self._substrands != new_substrands)
        self._substrands = new_substrands

        # Reverse the strand again to put the barbed end back at _substrands[-1]
        self.reverse()

        return changed

# Helper functions
def _join_strands(left, right):
    """
    Properly concatinates two strands (lists of substrands).
    """
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
        lc.extend(right)
    return lc

def _substrand_transition(probs, default_state):
    """
    Creates a short, 1 unit, strand containing the hydrolized transition from
    one substrand to the next.
    """
    if probs:
        return [(1, _choose_state(probs, mtrand.rand(), default_state))]
    else:
        return [(1, default_state)]

def _evolve_substrand(substrand, probs):
    """
    Performs random hydrolysis on a whole substrand.
    """
    num   = substrand[0]
    state = substrand[1]
    if not probs:
        return [(num, state)]
    rnums = mtrand.rand( num )
    states = map( lambda x: _choose_state( probs, x, state ), rnums )

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

def _choose_state(probs, num, default=None):
    """
    Selects a state from probs given an already generated random number, num.
    """
    for rate, state in probs:
        if num < rate:
            return state

    return default
