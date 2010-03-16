"""
    This module contains some very simple callables that can be used in both
random and vectorial hydrolysis models.
"""

import random

from util import choose_state

__all__ = ['BarbedPoly',   'PointedPoly',
           'BarbedDepoly', 'PointedDepoly',
           'CollectedRates', 'NoOp']

# No-op, do nothing instead of poly/depoly
def NoOp(strand):
    """
    Does nothing.
    """
    return 0

# Polymerization
class BarbedPoly(object):
    """
        Attaches a new monomer to the barbed end of the strand as determined
    by 'rates'.
    """
    def __init__(self, rates):
        self.rates = rates

    def __call__(self, strand):
        s = choose_state(self.rates, random.random())
        if s:
            strand.append(s)
            return 1
        else:
            return 0

class PointedPoly(object):
    """
        Attaches a new monomer to the pointed end of the strand as determined
    by 'rates'.
    """
    def __init__(self, rates):
        self.rates = rates

    def __call__(self, strand):
        s = choose_state(self.rates, random.random())
        if s:
            strand.appendleft(s)
            return 1
        else:
            return 0

# Depolymerization
class BarbedDepoly(object):
    """
        Removes a protomer to the barbed end of the strand as determined by
    'rates'.
    """
    def __init__(self, rates):
        self.rates = rates
    def __call__(self, strand):
        if random.random() < self.rates[strand[-1]]:
            strand.pop()
            return 1
        return 0

class PointedDepoly(object):
    """
        Removes a protomer to the pointed end of the strand as determined by
    'rates'.
    """
    def __init__(self, rates):
        self.rates = rates
    def __call__(self, strand):
        if random.random() < self.rates[strand[0]]:
            strand.popleft()
            return 1
        return 0

class CollectedRates(object):
    """
        Used to combine barbed and pointed end polymerization or
    depolymerization rates together to simplify the simulation.
    """
    def __init__(self, barbed, pointed):
        self.barbed  = barbed
        self.pointed = pointed
    def __call__(self, strand):
        return self.barbed(strand) + self.pointed(strand)
