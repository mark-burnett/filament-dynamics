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

import collections

from .base_classes import Observer


class ConcentrationObserver(Observer):
    __slots__ = ['_datastore']
    def __init__(self, *args, **kwargs):
        Observer.__init__(self, *args, **kwargs)

    def observe(self, time, simulation_state):
        for name, conc_obj in simulation_state.concentrations.iteritems():
            self.store(time, conc_obj.value(time), key=name)
