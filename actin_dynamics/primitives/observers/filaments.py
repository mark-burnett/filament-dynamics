#    Copyright (C) 2010-2011 Mark Burnett
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

from base_classes import ObserverMeasurement

class Length(ObserverMeasurement):
    __slots__ = []
    def observe(self, time, simulation_state):
        for name, filament in simulation_state.filaments.iteritems():
            length = len(filament)
            self.store(time, length, name)

class StateCount(ObserverMeasurement):
    __slots__ = ['state']
    def __init__(self, state=None, **kwargs):
        self.state = state
        ObserverMeasurement.__init__(self, **kwargs)

    def observe(self, time, simulation_state, results):
        for name, filament in simulation_state.filaments.iteritems():
            state_count = filament.state_count(self.state)
            self.store(time, state_count, name)

class WeightedStateTotal(ObserverMeasurement):
    __slots__ = ['weights']
    def __init__(self, label=None, **weights):
        self.weights = weights
        ObserverMeasurement.__init__(self, label=label)

    def observe(self, time, simulation_state):
        for name, filament in simulation_state.filaments.iteritems():
            value = sum(filament.state_count(simulation_state) * weight
                        for state, weight in self.weights.iteritems())
            self.store(time, value, name)
