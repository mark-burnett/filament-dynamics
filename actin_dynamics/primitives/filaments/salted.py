#    Copyright (C) 2011 Mark Burnett
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

import base_classes
from actin_dynamics.state.single_strand_filaments import Filament

class SaltedFixedLength(base_classes.FilamentFactory):
    def __init__(self, state=None, salt_state=None, salt_fraction=None,
            length=None, number=None, label=None):
        self.state = state
        self.salt_state = salt_state
        self.salt_fraction = float(salt_fraction)
        self.length = int(length)
        self.number = int(number)

    def create(self):
        return [Filament(self.state_iterator()) for i in xrange(self.number)]

    def state_iterator(self):
        count = 0
        while count < self.length:
            if random.random() < self.salt_fraction:
                yield self.salt_state
            else:
                yield self.state
            count += 1

class SaltedFixedLengthFromConcentrations(SaltedFixedLength):
    def __init__(self, concentration=None, filament_tip_concentration=None,
            *args, **kwargs):
        length = int(concentration / filament_tip_concentration)
        SaltedFixedLength.__init__(self, length=length, *args, **kwargs)
