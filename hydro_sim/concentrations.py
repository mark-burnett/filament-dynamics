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

from hydro_sim import events

class Concentration(object):
    def value(self):
        raise NotImplementedError()
    def initialize(self, pub):
        pass

class fixed_concentration(Concentration):
    __slots__ = ['conc']
    def __init__(self, conc):
        if conc < 0:
            raise ValueError('Negative concentrations not allowed.')
        self.conc = conc

    def value(self):
        return self.conc

class zero_concentration(Concentration):
    def value(self):
        return 0

class fixed_reagent(Concentration):
    __slots__ = ['pub', 'state', 'monomer_conc', 'filament_tip_conc']
    def __init__(self, state, initial_concentration, filament_tip_conc):
        self.state             = state
        self.monomer_conc      = initial_concentration
        self.filament_tip_conc = filament_tip_conc

    def value(self):
        return self.monomer_conc

    def initialize(self, pub):
        self.pub = pub
        pub.subscribe(self._update_poly,   events.polymerization)
        pub.subscribe(self._update_depoly, events.depolymerization)

    def _update_poly(self, event):
        if self.state == event.state:
            if self.monomer_conc >= self.filament_tip_conc:
                self.monomer_conc -= self.filament_tip_conc
                self.pub.publish(events.concentration_change(self.state))
            else:
                raise RuntimeError(
                'Could not polymerize without going to negative concentration.')

    def _update_depoly(self, event):
        if self.state == event.state:
            self.monomer_conc += self.filament_tip_conc
            self.pub.publish(events.concentration_change(self.state))
