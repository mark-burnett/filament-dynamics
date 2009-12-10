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
        self.poly_rate    = poly_rate
        self.hydro_rate   = hydro_rate
        self.release_rate = release_rate
        self.depoly_rates = (rT, rP, rD)

        self.poly_state  = poly_state
        self.window_size = 2

    def poly(self):
        return self.poly_rate
    def depoly(self, state):
        return self.depoly_rates[state]

    def transition(self, pointed_state, this_state):
        if T == this_state and T != pointed_state:
            return ((self.hydro_rate, P),)
        elif P == this_state and D == pointed_state:
            return ((self.release_rate, D),)
        return ()

    def transition_barbed(self, states):
        raise NotImplementedError
    def transition_pointed(self, states):
        st = states[0]
        if D == st:
            return ()
        elif T == st:
            newst = P
        else:
            newst = D
        return self.hydro_rates[st], newst

class VectoralRandom:
    def __init__(self, poly_rate, hydro_rate, release_rate, rT, rP, rD,
                 poly_state):
        self.poly_rate    = poly_rate
        self.hydro_rate   = hydro_rate
        self.release_rate = release_rate
        self.depoly_rates = (rT, rP, rD)

        self.poly_state  = poly_state
        self.window_size = 2

    def poly(self):
        return self.poly_rate
    def depoly(self, state):
        return self.depoly_rates[state]

    def transition(self, pointed_state, this_state):
        # Random release
        if P == this_state:
            return ((self.release_rate, D),)
        # Vectorial hydrolysis OK
        if T == this_state and P == pointed_state:
            return ((self.hydro_rate, P),)
        return ()

    def transition_barbed(self, states):
        raise NotImplementedError
    def transition_pointed(self, states):
        st = states[0]
        if D == st:
            return ()
        elif T == st:
            return (self.hydro_rate, P)
            newst = P
        return (self.release_rate, D)

class RandomRandom:
    def __init__(self, poly_rate, hydro_rate, release_rate, rT, rP, rD,
                 poly_state):
        self.poly_rate    = poly_rate
        self.hydro_rate   = hydro_rate
        self.release_rate = release_rate
        self.depoly_rates = (rT, rP, rD)

        self.poly_state  = poly_state
        self.window_size = 1

    def poly(self):
        return self.poly_rate
    def depoly(self, state):
        return self.depoly_rates[state]

    def transition(self, state):
        if T == state:
            return ((self.hydro_rate, P),)
        if P == state:
            return ((self.release_rate, D),)
        return ()

    def transition_barbed(self, states):
        raise NotImplementedError
    def transition_pointed(self, states):
        raise NotImplementedError

def _pars_to_class(pars, poly_state, cls):
    l = list(pars)
    l.append(poly_state)
    return cls(*l)

vv_from_list = lambda pars, ps: _pars_to_class(pars, ps, VectoralVectoral)
vr_from_list = lambda pars, ps: _pars_to_class(pars, ps, VectoralRandom)
rr_from_list = lambda pars, ps: _pars_to_class(pars, ps, RandomRandom)
