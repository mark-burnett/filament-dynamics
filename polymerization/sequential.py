import random

from compact_strand import CompactStrand as Strand
from compact_strand import cleanup_substrands

from util import choose_state

__all__ = ['Strand', 'Hydro']

class Hydro(object):
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
