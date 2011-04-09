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

import actin_dynamics.io.data
import actin_dynamics.io.object_graph
from actin_dynamics import io

import yaml

from actin_dynamics.primitives import analyses
from actin_dynamics import factories

from actin_dynamics.numerical import interpolation
from actin_dynamics.numerical import measurements


SEM = analyses.registry['StandardErrorMean']

def raw_sem_factory(measurement, label):
    return measurement

def get_measurement(raw_results, parameters, measurement_type=None,
                    measurement_name=None, scale_by=1, subtract=0):
    sem = SEM(sample_period=parameters['sample_period'],
              stop_time=parameters['duration'],
              interpolation_method='linear',
              measurement_name=measurement_name,
              measurement_type=measurement_type,
              scale_by=scale_by, subtract=subtract)
    return sem.perform(raw_results, raw_sem_factory)


def load_kinsim(filename, sample_period, duration):
    time, factin_d, pi_d, atp_d = io.data.load_data(filename)
    factin = time, factin_d
    pi = time, pi_d
    atp = time, atp_d

    sample_times = numpy.arange(0, duration + float(sample_period)/2,
                                sample_period)

    sampled_factin = interpolation.resample_measurement(factin, sample_times)
    sampled_pi     = interpolation.resample_measurement(pi, sample_times)
    sampled_atp    = interpolation.resample_measurement(atp, sample_times)

    return sampled_factin, sampled_pi, sampled_atp



# Helper code taken from old accessor stuff.
def get_scaled(parameter_set, name):
    basic = parameter_set['sem'][name]
    return measurements.scale(basic,
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
            og   = io.object_graph.parse_object_graph_file(open(og_file))
            parameters = yaml.load(open(par_file))

            raw_results = []
            for i in xrange(parameters['number_of_simulations']):
                simulation = factories.simulations.make_object_graph(og,
                        parameters)
                raw_results.append(simulation.run())

            length_sim = get_measurement(raw_results, parameters,
                                         measurement_type='filament',
                                         measurement_name='length',
                                         scale_by=parameters[
                                             'filament_tip_concentration'],
                                         subtract=parameters[
                                             'seed_concentration'])
            pi_sim     = get_measurement(raw_results, parameters,
                                         measurement_type='concentration',
                                         measurement_name='Pi')
            atp_sim    = get_measurement(raw_results, parameters,
                                         measurement_type='filament',
                                         measurement_name='atp_count',
                                         scale_by=parameters[
                                             'filament_tip_concentration'])

            factin_kin, pi_kin, atp_kin = load_kinsim(k_file,
                    parameters['sample_period'], parameters['duration'])

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
