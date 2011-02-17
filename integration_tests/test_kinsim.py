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

import numpy

from actin_dynamics import factories
from actin_dynamics import io
from actin_dynamics import run_support

from actin_dynamics.analysis import accessors
from actin_dynamics.analysis import interpolation
from actin_dynamics.analysis import utils


def load_kinsim(filename, sample_period, duration):
    factin, pi, atp = io.pollard.get_kinsim(filename)

    sample_times = numpy.arange(0, duration + float(sample_period)/2,
                                sample_period)

    sampled_factin = interpolation.resample_measurement(factin, sample_times)
    sampled_pi     = interpolation.resample_measurement(pi, sample_times)
    sampled_atp    = interpolation.resample_measurement(atp, sample_times)

    return sampled_factin, sampled_pi, sampled_atp



# Helper code taken from old accessor stuff.
def get_length(parameter_set):
    basic_length = parameter_set['sem']['length']
    subtracted_length = utils.add_number(basic_length,
            -basic_length[1][0])
    return utils.scale_measurement(subtracted_length,
            parameter_set['parameters']['filament_tip_concentration'])

def get_scaled(parameter_set, name):
    basic = parameter_set['sem'][name]
    return utils.scale_measurement(basic,
            parameter_set['parameters']['filament_tip_concentration'])



class TestKinsim(unittest.TestCase):
    def setUp(self):
        self.data_sets = [
                ('integration_tests/kinsim/pollard_og.yaml',
                 'integration_tests/kinsim/pollard_pars.yaml',
                 'integration_tests/kinsim/pollard_kinsim.dat')]

        self.percent_error = 0.01
        self.epsilon = 0.02


    def test_vs_kinsim(self):
        for og_file, par_file, k_file in self.data_sets:
            og   = io.parse_object_graph_file(open(og_file))
            pars = io.parse_parameters_file(open(par_file)).next()

            sg = factories.simulations.simulation_generator(og, pars)

            analyzed_set = run_support.typical_run(pars, sg)

            length_sim = get_length(analyzed_set)
            pi_sim     = analyzed_set['sem']['Pi']
            atp_sim    = get_scaled(analyzed_set, 'atp_count')

            factin_kin, pi_kin, atp_kin = load_kinsim(k_file,
                    pars['sample_period'], pars['simulation_duration'])

            self.assert_acceptable(length_sim, factin_kin)
            self.assert_acceptable(pi_sim, pi_kin)
            self.assert_acceptable(atp_sim, atp_kin)

    def assert_acceptable(self, sim, kin):
        for i, (t, v, e) in enumerate(zip(*sim)):
            self.assert_within(kin[1][i], v, e)


    def assert_within(self, kin, avg, error):
        ak = (avg + kin) / 2
        self.assertTrue(kin < avg
                              + 2 * error
                              + self.percent_error * ak
                              + self.epsilon)
        self.assertTrue(kin > avg
                              - 2 * error
                              - self.percent_error * ak
                              - self.epsilon)


if '__main__' == __name__:
    unittest.main()
