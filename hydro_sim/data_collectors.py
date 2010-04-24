#    Copyright (C) 2009 Mark Burnett
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

import hydro_sim.transitions.events

class LengthChange(object):
    __slots__ = ['pub', 'repository', 'count']
    def __init__(self, pub, repository):
        self.pub        = pub
        self.repository = repository
        self.count      = 0

    def initialize(self, data):
        self.pub.subscribe(self.increment,
                      hydro_sim.transitions.events.polymerization)
        self.pub.subscribe(self.decrement,
                      hydro_sim.transitions.events.depolymerization)

    def increment(self, event):
        self.count += 1
        self.repository.append((event.time, self.count))

    def decrement(self, event):
        self.count -= 1
        self.repository.append((event.time, self.count))
