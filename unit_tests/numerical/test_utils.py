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

import unittest

from actin_dynamics.numerical import utils

class RunningTotalTest(unittest.TestCase):
    def test_running_total(self):
        test_data = [[0, 1, 2, 3, 4, 5],
                     [7, 1, 2, 8],
                     [-5, 0, -2, 3]]
        answers   = [[0, 1, 3, 6, 10, 15],
                     [7, 8, 10, 18],
                     [-5, -5, -7, -4]]
        for a, d in zip(answers, test_data):
            self.assertEqual(a, list(utils.running_total(d)))

class RunningStatsTest(unittest.TestCase):
    def test_running_stats(self):
        test_data = [range(10),
                     range(4),
                     range(20)]
        a2 = float(sum(range(10)) + sum(range(4))) / 14
        a3 = float(sum(range(10)) + sum(range(4)) + sum(range(20))) / 34
        answers = [4.5, a2, a3]

        stats = utils.RunningStats()
        for a, d in zip(answers, test_data):
            stats.append(d)
            self.assertEqual(a, stats.mean)


if '__main__' == __name__:
    unittest.main()
