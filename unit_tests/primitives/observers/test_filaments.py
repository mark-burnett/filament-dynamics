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

import unittest

from actin_dynamics.primitives.observers import filaments
from actin_dynamics import simulation_strategy


class LengthObserverTest(unittest.TestCase):
    def setUp(self):
        self.o = filaments.Length(label='test label')
        self.results = {}
        self.o.initialize(self.results)

    def test_observe(self):
        ss = simulation_strategy.SimulationState(concentrations=None,
                filaments={'filamentA': range(10),
                           'filamentB': range(3)})

        self.o.observe(3.1, ss)
        self.assertEqual(self.results['test label']['filamentA'],
                         ([3.1], [10]))
        self.assertEqual(self.results['test label']['filamentB'],
                         ([3.1], [3]))

        ss.filaments['filamentA'].pop()

        self.o.observe(6.7, ss)
        self.assertEqual(self.results['test label']['filamentA'],
                         ([3.1, 6.7], [10, 9]))
        self.assertEqual(self.results['test label']['filamentB'],
                         ([3.1, 6.7], [3, 3]))


class StateCountObserverTest(unittest.TestCase):
    def setUp(self):
        self.o = filaments.StateCount(label='sc label', state=1)
        self.results = {}
        self.o.initialize(self.results)

    def test_observe(self):
        ss = simulation_strategy.SimulationState(concentrations=None,
                filaments={'filamentA': [1, 1, 2, 3, 1, 2, 1],
                           'filamentB': [2, 1, 1, 2, 3, 1]})

        self.o.observe(3.1, ss)
        self.assertEqual(self.results['sc label']['filamentA'],
                         ([3.1], [4]))
        self.assertEqual(self.results['sc label']['filamentB'],
                         ([3.1], [3]))

        ss.filaments['filamentA'][0]  = 2
        ss.filaments['filamentA'][-1] = 2
        ss.filaments['filamentB'][3]  = 1

        self.o.observe(6.7, ss)
        self.assertEqual(self.results['sc label']['filamentA'],
                         ([3.1, 6.7], [4, 2]))
        self.assertEqual(self.results['sc label']['filamentB'],
                         ([3.1, 6.7], [3, 4]))


class WeightedStateTotalTest(unittest.TestCase):
    def setUp(self):
        self.o = filaments.WeightedStateTotal(label='sc label',
                a=1, b=2, c=3)
        self.results = {}
        self.o.initialize(self.results)

    def test_observe(self):
        ss = simulation_strategy.SimulationState(concentrations=None,
                filaments={'filamentA': ['a', 'a', 'b', 'c', 'a', 'b', 'a'],
                           'filamentB': ['b', 'a', 'a', 'b', 'c', 'a']})

        self.o.observe(3.1, ss)
        self.assertEqual(self.results['sc label']['filamentA'],
                         ([3.1], [11]))
        self.assertEqual(self.results['sc label']['filamentB'],
                         ([3.1], [10]))

        ss.filaments['filamentA'][1] = 'c'
        ss.filaments['filamentB'][3] = 'a'

        self.o.observe(6.7, ss)
        self.assertEqual(self.results['sc label']['filamentA'],
                         ([3.1, 6.7], [11, 13]))
        self.assertEqual(self.results['sc label']['filamentB'],
                         ([3.1, 6.7], [10, 9]))

class FilamentCounterTest(unittest.TestCase):
    def setUp(self):
        self.o = filaments.FilamentCounter(label='filament count')
        self.results = {}
        self.o.initialize(self.results)

    def test_observe(self):
        ss = simulation_strategy.SimulationState(concentrations=None,
                filaments={'filamentA': range(3),
                           'filamentB': range(2),
                           'filamentC': range(4)})
        self.o.observe(3.1, ss)
        self.assertEqual(self.results['filament count'],
            ([3.1], [3]))

        ss.filaments['filamentD'] = range(7)
        self.o.observe(6.7, ss)
        self.assertEqual(self.results['filament count'],
                         ([3.1, 6.7], [3, 4]))

        del ss.filaments['filamentA']
        del ss.filaments['filamentC']
        self.o.observe(8.3, ss)
        self.assertEqual(self.results['filament count'],
                         ([3.1, 6.7, 8.3], [3, 4, 2]))



if '__main__' == __name__:
    unittest.main()
