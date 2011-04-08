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

from base_classes import FilamentFactory as _FilamentFactory

from actin_dynamics.state.single_strand_filaments import Filament
#from actin_dynamics.state.segmented_filaments import SegmentedFilament, BasicSegment
#from actin_dynamics.state.edge_tracking_filaments import EdgeTrackingFilament

class SingleStateFixedLength(_FilamentFactory):
    def __init__(self, state=None, length=None, number=None, label=None):
        self.state = state
        self.length = int(length)
        self.number = int(number)

        _FilamentFactory.__init__(self, label=label)

    def create(self):
#        return [EdgeTrackingFilament(counts=[self.length], states=[self.state])
#                for i in xrange(self.number)]
#        return [SegmentedFilament(BasicSegment(state=self.state,
#                                               count=self.length))
#                for i in xrange(self.number)]

        return [Filament(itertools.repeat(self.state, self.length))
                for i in xrange(self.number)]

class SingleStateFixedLengthFromConcentrations(SingleStateFixedLength):
    def __init__(self, state=None, concentration=None,
                 filament_tip_concentration=None, number=None, label=None):
        length = int(concentration / filament_tip_concentration)
        SingleStateFixedLength.__init__(self, state=state, length=length,
                                        number=number, label=label)


class NormalDistribution(_FilamentFactory):
    def __init__(self, mean=None, standard_deviation=None,
                 state=None, number=None, label=None):
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.state = state
        self.number = number

        _FilamentFactory.__init__(self, label=label)

    def create(self):
        return [Filament(itertools.repeat(self.state,
                    int(random.normalvariate(self.mean, self.standard_deviation))))
                for i in xrange(int(self.number))]
