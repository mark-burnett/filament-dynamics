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

from states import ChemicalState, MechanicalState, ProtomerState
from simple_rates import _pars_to_class

T = ChemicalState.ATP
P = ChemicalState.ADPPi
D = ChemicalState.ADP

O = MechanicalState.OPEN
C = MechanicalState.CLOSED

class VecMRandC:
    def __init__(self, poly_rate,
                 hydro_rate, release_rate, hydro_inhibition, release_inhibition,
                 open_rate, close_rate, mechanical_inhibition,
                 rT, rP, rD, poly_state):
        self.hydro_rate   = hydro_rate
        self.release_rate = release_rate

        self.hydro_inhibition   = hydro_inhibition
        self.release_inhibition = release_inhibition

        self.open_rate  = open_rate
        self.close_rate = close_rate

        self.mechanical_inhibition = mechanical_inhibition

        self.poly_rate    = poly_rate
        self.depoly_rates = (rT, rP, rD)

        self.poly_state  = poly_state
        self.window_size = 3

    def poly(self):
        return self.poly_rate
    def depoly(self, state):
        return self.depoly_rates[state.chemical_state]

    def _hydro_transition(self, this_state):
        # Figure out chemical state changes
        if T is this_state.chemical_state:
            next_cs = P
            if this_state.mechanical_state is O:
                chemical_probability = self.hydro_rate * self.hydro_inhibition
            else:
                chemical_probability = self.hydro_rate
        elif P is this_state.chemical_state:
            next_cs = D
            if this_state.mechanical_state is C:
                chemical_probability = self.release_rate*self.release_inhibition
            else:
                chemical_probability = self.release_rate
        else:
            return None
        return chemical_probability, next_cs

    def transition(self, pointed_neighbor, this_state, barbed_neighbor):
        # Figure out mechanical state changes
        if this_state.mechanical_state is O:
            next_ms = C
            mechanical_probability = self.close_rate
        else:
            next_ms = O
            mechanical_probability = self.open_rate

        if pointed_neighbor.mechanical_state is this_state.mechanical_state:
            mechanical_probability *= self.mechanical_inhibition
        if barbed_neighbor.mechanical_state is this_state.mechanical_state:
            mechanical_probability *= self.mechanical_inhibition

        return _combine_probs(self._hydro_transition(this_state),
                              mechanical_probability, next_ms,
                              this_state)

    def transition_barbed(self, states):
        pointed_neighbor = states[0]
        this_state       = states[1]
        # Figure out mechanical state changes
        if this_state.mechanical_state is O:
            next_ms = C
            mechanical_probability = self.close_rate
        else:
            next_ms = O
            mechanical_probability = self.open_rate

        if pointed_neighbor.mechanical_state is this_state.mechanical_state:
            mechanical_probability *= self.mechanical_inhibition

        return _combine_probs(self._hydro_transition(this_state),
                              mechanical_probability, next_ms,
                              this_state)
    def transition_pointed(self, states):
        this_state      = states[0]
        barbed_neighbor = states[1]
        # Figure out mechanical state changes
        if this_state.mechanical_state is O:
            next_ms = C
            mechanical_probability = self.close_rate
        else:
            next_ms = O
            mechanical_probability = self.open_rate

        if barbed_neighbor.mechanical_state is this_state.mechanical_state:
            mechanical_probability *= self.mechanical_inhibition

        return _combine_probs(self._hydro_transition(this_state),
                              mechanical_probability, next_ms,
                              this_state)

def _combine_probs(t, mechanical_probability, next_ms, this_state):
    if t:
        chemical_probability, next_cs = t
        # Combine
        return ((mechanical_probability,
                    ProtomerState(this_state.chemical_state, next_ms)),
                (chemical_probability + mechanical_probability,
                    ProtomerState(next_cs, this_state.mechanical_state)))
    else:
        return ((mechanical_probability,
                    ProtomerState(this_state.chemical_state, next_ms)),)

vmrc_from_list = lambda pars, ps: _pars_to_class(pars, ps, VecMRandC)
