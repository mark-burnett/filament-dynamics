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

import util
import kmc.simulation

__all__ = ['simulation']

def simulation(transitions_factory,
               end_conditions_factory,
               measuremets_factory):
    while True:
        # Construct publisher.
        # This assures that each simulation acts independently.
        pub = util.observer.Publisher()

        # Construct transitions.
        transitions = transitions_factory(pub)

        # Construct end conditions.
        end_conditions = end_conditions_factory(pub)

        # Construct data_collectors.
        measurements, data_repository = measuremets_factory(pub)

        # Construct simulation.
        yield (kmc.simulation.Simulation(transitions, measurements,
                                         end_conditions),
               data_repository)
