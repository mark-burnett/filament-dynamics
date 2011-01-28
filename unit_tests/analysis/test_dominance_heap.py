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

import unittest

from actin_dynamics.analysis import dominance_heap

class TestRankedObject(unittest.TestCase):
    def setUp(self):
        self.a = dominance_heap.RankedObject(None, None)
        self.b = dominance_heap.RankedObject(None, None)
        self.c = dominance_heap.RankedObject(None, None)

    def test_initialization(self):
        self.assertEqual(0, len(self.a.trumps))
        self.assertEqual(0, len(self.a.trails))

        self.assertEqual(0, len(self.b.trumps))
        self.assertEqual(0, len(self.b.trails))

        self.assertEqual(0, len(self.c.trumps))
        self.assertEqual(0, len(self.c.trails))


    def test_comparison(self):
        self.assertEqual(0, cmp(self.a, self.b))
        self.assertEqual(0, cmp(self.a, self.c))
        self.assertEqual(0, cmp(self.c, self.b))

        self.a.trails.add(self.b)
        self.b.trumps.add(self.a)

        self.assertEqual(-1, cmp(self.a, self.b))
        self.assertEqual(-1, cmp(self.a, self.c))
        self.assertEqual(-1, cmp(self.c, self.b))

        self.assertEqual( 1, cmp(self.b, self.a))
        self.assertEqual( 1, cmp(self.c, self.a))
        self.assertEqual( 1, cmp(self.b, self.c))

    def test_remove_trails(self):
        # Make sure we don't raise exceptions when empty.
        self.c.remove_references(self.a)

        self.a.trails.add(self.b)
        self.assertEqual(1, len(self.a.trails))

        # Make sure nothing happens when we remove something non-existant.
        self.a.remove_references(self.c)
        self.assertEqual(1, len(self.a.trails))

        self.a.remove_references(self.b)
        self.assertEqual(0, len(self.a.trails))

    def test_remove_trumps(self):
        # Make sure we don't raise exceptions when empty.
        self.c.remove_references(self.a)

        self.a.trumps.add(self.b)
        self.assertEqual(1, len(self.a.trumps))

        # Make sure nothing happens when we remove something non-existant.
        self.a.remove_references(self.c)
        self.assertEqual(1, len(self.a.trumps))

        self.a.remove_references(self.b)
        self.assertEqual(0, len(self.a.trumps))

class TestRankedPopulation(unittest.TestCase):
    def setUp(self):
        self.population = dominance_heap.RankedPopulation()

        self.costs = [(90, 30, 50), # Doesn't trump
                      (60, 20, 40), # Trumps 0,
                      (50, 20, 45), # Trumps 0,
                      (55, 15, 35), # Trumps 0, 1,
                      (46, 18, 42), # Trumps 0, 2
                      (48, 12, 30), # Trumps 0, 2, 3
                      (40, 10, 41)] # Trumps 0, 2, 3, 4

        self.trumps = [[],
                       [0],
                       [0],
                       [0, 1],
                       [0, 2],
                       [0, 1, 2, 3],
                       [0, 2, 4]]

        self.trails = [[1, 2, 3, 4, 5, 6],
                       [3, 5],
                       [4, 5, 6],
                       [5],
                       [6],
                       [],
                       []]

        self.sort_order = [5, 6, 3, 4, 1, 2, 0]
        self.reverse_order = [0, 2, 1, 3, 4, 6, 5]
        
    def build_population(self):
        for i, c in enumerate(self.costs):
            self.population.push(i, c)


    def test_trumps(self):
        for c, trumps in zip(self.costs, self.trumps):
            for i in xrange(len(self.costs)):
                if i in trumps:
                    self.assertTrue(dominance_heap.trumps(c, self.costs[i]),
                                    str((c, i, self.costs[i])))
                else:
                    self.assertFalse(dominance_heap.trumps(c, self.costs[i]),
                                     str((c, i, self.costs[i])))

    def test_trails(self):
        for c, trails in zip(self.costs, self.trails):
            for i in xrange(len(self.costs)):
                if i in trails:
                    self.assertTrue(dominance_heap.trails(c, self.costs[i]),
                                    str((c, i, self.costs[i])))
                else:
                    self.assertFalse(dominance_heap.trails(c, self.costs[i]),
                                     str((c, i, self.costs[i])))

    # Integration test.
    def test_whole_sort(self):
        self.build_population()

        # Make sure each push got the right trails/trumps setup.
        for m in self.population.members:
            index = self.costs.index(m.cost)
            trumps = self.trumps[index]
            trails = self.trails[index]

            self.assertEqual(len(m.trumps), len(trumps),
                             str(([t.cost for t in m.trumps],
                                  [self.costs[t] for t in trumps])))

            self.assertEqual(len(m.trails), len(trails),
                             str(([t.cost for t in m.trails],
                                  [self.costs[t] for t in trails])))

        # Verify whole sort order.
        self.assertEqual(self.sort_order,
                         [m.parameters
                          for m in self.population.get_best(len(self.costs))])

        # Verify reverse sort order.
        self.assertEqual(self.reverse_order,
                         [m.parameters
                          for m in self.population.get_worst(len(self.costs))])

    def test_get_best(self):
        self.build_population()
        best = self.population.get_best()
        self.assertEqual(best.parameters, 5)
        self.assertEqual(best.cost, self.costs[5])

    def test_get_worst(self):
        self.build_population()
        worst = self.population.get_worst()
        self.assertEqual(worst.parameters, 0)
        self.assertEqual(worst.cost, self.costs[0])
