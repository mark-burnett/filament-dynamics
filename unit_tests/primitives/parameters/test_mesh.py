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

from actin_dynamics.primitives.parameters import mesh


class ParameterMeshTest(unittest.TestCase):
    def test_mesh_generator(self):
        lower_bound = 3.2
        upper_bound = 7.2
        step_size   = 0.5
        g = mesh.mesh_generator(lower_bound, upper_bound, step_size)

        self.assertEqual(g, iter(g))

        values = list(g)
        self.assertEqual(9, len(values))
        self.assertEqual(lower_bound, values[0])
        self.assertAlmostEqual(upper_bound, values[-1])


    def test_mesh_step_size(self):
        lower_bound = 3.2
        upper_bound = 7.2
        step_size   = 0.5
        m = mesh.Mesh(lower_bound=lower_bound, upper_bound=upper_bound,
                      step_size=step_size)

        g = iter(m)
        self.assertEqual(g, iter(g))

        values = list(g)
        self.assertEqual(9, len(values))
        self.assertEqual(lower_bound, values[0])
        self.assertAlmostEqual(upper_bound, values[-1])

    def test_mesh_num_points(self):
        lower_bound = 3.2
        upper_bound = 7.2
        num_points  = 10

        m = mesh.Mesh(lower_bound=lower_bound, upper_bound=upper_bound,
                      num_points=num_points)

        g = iter(m)
        self.assertEqual(g, iter(g))

        values = list(g)
        self.assertEqual(num_points, len(values))
        self.assertEqual(lower_bound, values[0])
        self.assertAlmostEqual(upper_bound, values[-1])


if '__main__' == __name__:
    unittest.main()
