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

import util
import itertools
import random

def single_state(model_states, simulation_states, size):
    state = util.states.match(model_states, simulation_states)
    while True:
        # XXX watch out for the list/deque problem (pointed end effects)
        yield list(itertools.repeat(state, size))

def random_states(model_states, simulation_states, size):
    states = [util.states.match(model_states, s) for s in simulation_states]
    while True:
        # XXX watch out for the list/deque problem (pointed end effects)
        yield [random.choice(states) for n in xrange(size)]
