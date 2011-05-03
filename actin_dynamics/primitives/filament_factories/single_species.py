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

import itertools
import random

from base_classes import FilamentFactory

from actin_dynamics.state.single_strand_filaments import Filament

__all__ = ['SingleSpeciesFixedLength', 'SingleSpeciesFixedLengthFromConcentrations',
        'NormalDistribution']

class SingleSpeciesFixedLength(FilamentFactory):
    def __init__(self, species=None, length=None, number=None, label=None):
        self.species = species
        self.length = int(length)
        self.number = int(number)

        FilamentFactory.__init__(self, label=label)

    def create(self):
        return [Filament(itertools.repeat(self.species, self.length))
                for i in xrange(self.number)]

class SingleSpeciesFixedLengthFromConcentrations(SingleSpeciesFixedLength):
    def __init__(self, concentration=None, filament_tip_concentration=None,
                 *args, **kwargs):
        length = int(concentration / filament_tip_concentration)
        SingleSpeciesFixedLength.__init__(self, length=length, *args, **kwargs)
