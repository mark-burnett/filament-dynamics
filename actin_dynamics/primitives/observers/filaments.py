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

from .base_classes import Observer

__all__ = ['Length', 'SpeciesCount', 'WeightedSpeciesTotal', 'FilamentCounter']

class Length(Observer):
    __slots__ = []
    def observe(self, time, simulation_state):
        for name, filament in simulation_state.filaments.iteritems():
            length = len(filament)
            self.store(time, length, key=name)

class SpeciesCounter(Observer):
    __slots__ = ['species']
    def __init__(self, species=None, *args, **kwargs):
        self.species = species
        Observer.__init__(self, *args, **kwargs)

    def observe(self, time, simulation_state):
        for name, filament in simulation_state.filaments.iteritems():
            # XXX straighten out count/state_count
            species_count = filament.count(self.species)
            self.store(time, species_count, key=name)

class WeightedSpeciesTotal(Observer):
    __slots__ = ['weights']
    def __init__(self, label=None, *args, **weights):
        self.weights = weights
        Observer.__init__(self, label=label, *args)

    def observe(self, time, simulation_state):
        for name, filament in simulation_state.filaments.iteritems():
            value = sum(filament.count(species) * weight
                        for species, weight in self.weights.iteritems())
            self.store(time, value, key=name)

class FilamentCounter(Observer):
    __slots__ = []
    def __init__(self, *args, **kwargs):
        Observer.__init__(self, datastore_type='timecourse', *args, **kwargs)

    def observe(self, time, simulation_state):
        self.store(time, len(simulation_state.filaments))
