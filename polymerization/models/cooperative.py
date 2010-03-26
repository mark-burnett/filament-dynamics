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

import random

from polymerization.rates.util import choose_state

__all__ = ['hydrolysis', 'strand']

class Hydrolysis(object):
    def __init__(self, rates):
        self.rates = rates

    def __call__(self, s):
        for i in xrange(len(s) - 1):
            new_state = choose_state(self.rates[s[i] + s[i+1]], random.random())
            if new_state:
                s[i] = new_state

# Lowercase alias
hydrolysis = Hydrolysis

# Use the strand factory from random_model
from random_model import strand
