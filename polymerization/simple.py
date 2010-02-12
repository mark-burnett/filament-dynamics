import random

from util import choose_state

__all__ = ['BarbedPoly',   'PointedPoly',
           'BarbedDepoly', 'PointedDepoly',
           'CollectedRates', 'NoOp']

# No-op, do nothing instead of poly/depoly
def NoOp(strand):
    return 0

# Polymerization
class BarbedPoly(object):
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
    def __init__(self, rates):
        self.rates = rates
    def __call__(self, strand):
        if random.random() < self.rates[strand[-1]]:
            strand.pop()
            return 1
        return 0

class PointedDepoly(object):
    def __init__(self, rates):
        self.rates = rates
    def __call__(self, strand):
        if random.random() < self.rates[strand[0]]:
            strand.popleft()
            return 1
        return 0

class CollectedRates(object):
    def __init__(self, Barbed, Pointed):
        self.Barbed  = Barbed
        self.Pointed = Pointed
    def __call__(self, strand):
        return self.Barbed(strand) + self.Pointed(strand)

# Hydrolysis
class Hydro(object):
    def __init__(self, rates, strand_factory):
        self.rates = rates
        self.strand_factory = strand_factory

    def create_strand(self, size):
        return self.strand_factory(size)

    def __call__(self, strand):
        raise NotImplementedError()
