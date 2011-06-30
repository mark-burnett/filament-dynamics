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

from base_classes import Measurement as _Measurement

from actin_dynamics import logger
_log = logger.getLogger(__file__)

class Length(_Measurement):
    def __init__(self, **kwargs):
        _Measurement.__init__(self, **kwargs)

    def perform(self, time, filaments):
        for filament in filaments:
            length = len(filament)
            self.store(time, length, filament)

class StateCount(_Measurement):
    __slots__ = ['state']
    def __init__(self, state=None, **kwargs):
        self.state = state
        _Measurement.__init__(self, **kwargs)

    def perform(self, time, filaments):
        for filament in filaments:
            state_count = filament.state_count(self.state)
            self.store(time, state_count, filament)

class WeightedStateTotal(_Measurement):
    __slots__ = ['weights']
    def __init__(self, label=None, sample_period=None, **weights):
        self.weights = weights
        _Measurement.__init__(self, label=label, sample_period=sample_period)

    def perform(self, time, filaments):
        for filament in filaments:
            value = sum(filament.state_count(state) * weight
                        for state, weight in self.weights.iteritems())
            self.store(time, value, filament)

class StateCountSum(_Measurement):
    __slots__ = ['base_state', 'prefix']
    def __init__(self, base_state=None, prefix=None, **kwargs):
        self.base_state = base_state
        self.prefix     = prefix
        _Measurement.__init__(self, **kwargs)

    def perform(self, time, filaments):
        for filament in filaments:
            state_count  = filament.state_count(self.base_state)
            state_count += filament.state_count(self.prefix + self.base_state)
            self.store(time, state_count, filament)

class StateDistributionMean(_Measurement):
    __slots__ = ['state']
    def __init__(self, state=None, **kwargs):
        self.state = state
        _Measurement.__init__(self, **kwargs)

    def perform(self, time, filaments):
        for filament in filaments:
            value = float(filament.state_distribution_mean(self.state))
            self.store(time, value, filament)

class StateDistributionSTD(_Measurement):
    __slots__ = ['state']
    def __init__(self, state=None, **kwargs):
        self.state = state
        _Measurement.__init__(self, **kwargs)

    def perform(self, time, filaments):
        for filament in filaments:
            value = float(filament.state_distribution_std(self.state))
            self.store(time, value, filament)

class TipState(_Measurement):
    __slots__ = ['state_translation']
    def __init__(self, label=None, sample_period=None,
                 **state_translation):
        self.state_translation = state_translation
        _Measurement.__init__(self, label=label,
                sample_period=sample_period)

    def perform(self, time, filaments):
        for filament in filaments:
            value = self.state_translation[filament[-1]]
            self.store(time, value, filament)
