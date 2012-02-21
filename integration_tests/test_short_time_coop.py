#    Copyright (C) 2012 Mark Burnett
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

import csv

import numpy
import yaml

#import actin_dynamics.io.data
#from actin_dynamics import io

import actin_dynamics.factories.simulations
from actin_dynamics import factories


class TestShortTimeCooperative(unittest.TestCase):
    def setUp(self):
        og_config  = open('integration_tests/short_time/st_og.yaml').read()
        par_config = open('integration_tests/short_time/st_pars.yaml').read()

        self.og = yaml.safe_load(og_config)
        self.pars = yaml.safe_load(par_config)

        self.initial_length = (self.pars['seed_concentration'] /
                self.pars['filament_tip_concentration'])

        self.expected_times = []
        self.expected_T = []
        self.expected_D = []
        for t, T, D in csv.reader(open('integration_tests/short_time/st_expected.csv')):
            self.expected_times.append(float(t))
            self.expected_T.append(float(T))
            self.expected_D.append(float(D) + self.initial_length)

        self.percent_error = 0.01
        self.epsilon = 0.01

    def test_short_time(self):
        simulation = factories.simulations.make_object_graph(self.og, self.pars)
        simulation_results = simulation.run()

        sample_period = self.pars['sample_period']
        t = numpy.arange(0, self.pars['duration'] + float(sample_period)/2, sample_period)

        # Length
        expected_length = (self.pars['barbed_atp_polymerization_rate']
                * self.pars['atp_concentration'] * t) + self.initial_length

        simulated_length = self.extract_measurement(simulation_results,
                'length', self.pars)
        self.assert_acceptable(simulated_length, expected_length)

        # ATP
        simulated_atp_count = self.extract_measurement(simulation_results,
                'atp_count', self.pars)
        self.assert_acceptable(simulated_atp_count, self.expected_T)

        # ADP
        simulated_adp_count = self.extract_measurement(simulation_results,
                'adp_count', self.pars)
        self.assert_acceptable(simulated_adp_count, self.expected_D)

    def extract_measurement(self, simulation_results, measurement_name, parameters,
        scale_by=1, subtract=0):
        m_results = simulation_results[measurement_name]
        times = m_results.get_times()

        means = m_results.get_means()
        means = [m * scale_by - subtract for m in means]

        sqrt_n_m_1 = 1 / numpy.sqrt(parameters['number_of_filaments'])
        errors = [m * sqrt_n_m_1 for m in means]

        return (times, means, errors)

    def assert_acceptable(self, sim, expect):
        for i, (t, v, e) in enumerate(zip(*sim)):
            self.assert_within(expect[i], v, e)

    def assert_within(self, expect, avg, error):
        ak = (avg + expect) / 2
        self.assertLess(expect, avg
                              + 2 * error
                              + self.percent_error * ak
                              + self.epsilon)
        self.assertGreater(expect, avg
                              - 2 * error
                              - self.percent_error * ak
                              - self.epsilon)
