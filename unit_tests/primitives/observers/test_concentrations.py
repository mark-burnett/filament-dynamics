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

from actin_dynamics.primitives.observers import concentrations
from actin_dynamics import simulation_strategy

from unit_tests.mocks.concentrations import MockConcentration


class ConcentrationObserverTest(unittest.TestCase):
    def setUp(self):
        self.co = concentrations.ConcentrationObserver(label='test_label')
        self.results = {}
        self.co.initialize(self.results)

    def test_initialize(self):
        self.assertTrue(isinstance(self.results['concentrations'], dict))
        # Verify results is a defaultdict
        self.assertEqual(([], []),
                self.results['concentrations']['test species'])

    def test_observe(self):
        ss = simulation_strategy.SimulationState(filaments=None,
                concentrations={'speciesA': MockConcentration(value=3),
                                'speciesB': MockConcentration(value=2)})

        self.co.observe(7.2, ss)

        for conc_obj in ss.concentrations.itervalues():
            self.assertEqual(1, conc_obj.value_access_count)

        self.assertEqual(([7.2], [3]),
                self.results['concentrations']['speciesA'])

        self.assertEqual(([7.2], [2]),
                self.results['concentrations']['speciesB'])


        self.co.observe(13.6, ss)

        for conc_obj in ss.concentrations.itervalues():
            self.assertEqual(2, conc_obj.value_access_count)

        self.assertEqual(([7.2, 13.6], [3, 3]),
                self.results['concentrations']['speciesA'])

        self.assertEqual(([7.2, 13.6], [2, 2]),
                self.results['concentrations']['speciesB'])



if '__main__' == __name__:
    unittest.main()
