#    Copyright (C) 2010 Mark Burnett, David Morton
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

import heapq

from itertools import izip

class RankedObject(object):
    __slots__ = ['trails', 'trumps', 'cost', 'parameters']
    def __init__(self, parameters, cost):
        self.trails = set()
        self.trumps = set()
        self.cost = cost
        self.parameters = parameters

    def remove_references(self, other):
        self.trails.discard(other)
        self.trumps.discard(other)

    def __str__(self):
        return 'trails: %s, trumps: %s, cost: %s' % (
                len(self.trails), len(self.trumps), self.cost)

    def __cmp__(self, sister):
        return cmp((-len(self.trails),   len(self.trumps)),
                   (-len(sister.trails), len(sister.trumps)))


class RankedPopulation(object):
    def __init__(self, members=None, max_length=500):
        self.max_length = max_length
        self._up_to_date = False

        if members is not None:
            self.members = members
        else:
            self.members = []

    def push(self, new_parameters, new_cost):
        new_item = RankedObject(new_parameters, new_cost)
        for m in self.members:
            if trumps(new_cost, m.cost):
                new_item.trumps.add(m)
                m.trails.add(new_item)
            elif trails(new_cost, m.cost):
                new_item.trails.add(m)
                m.trumps.add(new_item)

        self.members.append(new_item)
        self._up_to_date = False

        # We can't simply use push_pop -- the hash doesn't stay invariant.
        if self.max_length and len(self.members) > self.max_length:
            return self.pop()

        return None

    def pop(self):
        self._update()
        result = heapq.heappop(self.members)
        for m in self.members:
            m.remove_references(result)

        return result

    
    def get_best(self, number=1):
        if 1 == number:
            return max(self.members)
        else:
            self._update()
            return heapq.nlargest(number, self.members)

    def get_worst(self, number=1):
        if 1 == number:
            return min(self.members)
        else:
            self._update()
            return heapq.nsmallest(number, self.members)


    def _update(self):
        if not self._up_to_date:
            heapq.heapify(self.members)
            self._up_to_date = True


# Smaller is better.  We're treating everything as a residual.
def trumps(cost1, cost2):
    return all(f1 < f2 for f1, f2 in izip(cost1, cost2))

def trails(cost1, cost2):
    return all(f1 > f2 for f1, f2 in izip(cost1, cost2))
