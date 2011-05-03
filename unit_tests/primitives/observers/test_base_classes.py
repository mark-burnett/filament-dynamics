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

from actin_dynamics.primitives.observers import base_classes
from actin_dynamics import simulation_strategy


class FilamentObserverTest(unittest.TestCase):
    def setUp(self):
        self.o = base_classes.FilamentObserver(label='test label')
        self.results = {'filaments': {}}
        self.o.initialize(self.results)

    def test_initialize(self):
        self.assertTrue(isinstance(self.results['filaments'], dict))
        self.assertTrue(isinstance(self.results['filaments']['test label'], dict))

    def test_store(self):
        self.o.store('time1', 'value1', 'filamentA')
        self.assertEqual(self.results['filaments']['test label']['filamentA'],
                (['time1'], ['value1']))


if '__main__' == __name__:
    unittest.main()
