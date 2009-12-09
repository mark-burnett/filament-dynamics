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

from states import ChemicalState

T = ChemicalState.ATP
P = ChemicalState.ADPPi
D = ChemicalState.ADP

class VectoralVectoral:
    def __init__(self, poly_rate, hydro_rate, release_rate, rT, rP, rD,
                 poly_state):
        self.poly_rate = poly_rate
        self.hydro_rates  = (hydro_rate, release_rate)
        self.depoly_rates = (rT, rP, rD)

        self.poly_state  = poly_state
        self.window_size = 2

    def poly(self):
        return self.poly_rate
    def depoly(self, state):
        return self.depoly_rates[state]

    def transition(self, states):
        pointed_state = states[0]
        this_state    = states[1]
        if pointed_state > this_state:
            return ((self.hydro_rates[this_state], pointed_state),)
        return ()

    def transition_barbed(self, states):
        raise NotImplementedError
    def transition_pointed(self, states):
        st = states[0]
        if D == st:
            return ()
        elif T == st:
            newst = P
        elif P == st:
            newst = D
        return self.hydro_rates[st], newst

def vv_from_list(pars, poly_state):
    l = list(pars)
    l.append(poly_state)
    return VectoralVectoral(*l)
