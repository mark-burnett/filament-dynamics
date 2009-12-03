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

from itertools import izip
from states import ChemicalState

def uncoupled(states, rates):
    """
    Generates an uncoupled hydrolysis rate dictionary for use in the coupled
    simulation.
    """
    d = {}
    for s1, r in izip(states, rates):
        d[(s1, None)] = r
        for s2 in states:
            d[(s1, s2)] = r
    return d

def vectoral(wh, wr):
    """
    Generates a simple vectoral hydrolysis dictionary.

    wh is the rate of cleaving a phosphate from ATP
    wr is the rate of releasing that phosphate from ADPPi
    """
    T = ChemicalState.ATP
    P = ChemicalState.ADPPi
    D = ChemicalState.ADP
    return {
            (T,T): [],
            (T,P): [(wh, P)],
            (T,D): [(wh, P)],
            (P,T): [],
            (P,P): [],
            (P,D): [(wr, D)],
            (D,T): [],
            (D,P): [],
            (D,D): [],
            (T,None): [],
            (P,None): [],
            (D,None): [] }


def build_lipowsky_coupled(wh, rhoh, wr, rhor):
    """
    Generates a dicitonary for doing Lipowsky's coupled hydrolysis model:
    PRL 103, 048102 (2009)

    wh is the rate of cleaving a phosphate from ATP
    wr is the rate of releasing that phosphate from ADPPi

    the rho's are the suppression rates for hydrolysis and removal
    """
    T = ChemicalState.ATP
    P = ChemicalState.ADPPi
    D = ChemicalState.ADP
    return {
            (T,T): [(rhoh * wh, P)],
            (T,P): [(       wh, P)],
            (T,D): [(       wh, P)],
            (P,T): [(rhor * wr, D)],
            (P,P): [(rhor * wr, D)],
            (P,D): [(       wr, D)],
            (D,T): [],
            (D,P): [],
            (D,D): [],
            (T,None): [],
            (P,None): [],
            (D,None): [] }
