//    Copyright (C) 2012 Mark Burnett
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include <gtest/gtest.h>

#include <vector>
#include <boost/assign/std/vector.hpp>

// Bring operator+= into the namespace
using namespace boost::assign;

#include "test_states.h"

#include "concentrations/concentration.h"
#include "concentrations/fixed_reagent.h"

#include "measurements/concentration.h"

using namespace stochastic;

class ConcentrationMeasurementTest : public testing::Test {
    protected:
        virtual void SetUp() {
            concentrations[zero] = concentrations::Concentration::ptr_t(
                    new concentrations::FixedReagent(4, 1));
            concentrations[one] = concentrations::Concentration::ptr_t(
                    new concentrations::FixedReagent(2, 1, 2));
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(ConcentrationMeasurementTest, Initialize) {
    measurements::Concentration m0(zero, 1);
    measurements::Concentration m1(one, 1);

    m0.initialize(filaments, concentrations);
    m1.initialize(filaments, concentrations);

    std::vector<double> results0(m0.get_means());
    std::vector<double> results1(m1.get_means());

    EXPECT_EQ(0, m0.previous_time);
    EXPECT_EQ(1, results0.size());
    EXPECT_DOUBLE_EQ(4, results0[0]);

    EXPECT_EQ(0, m1.previous_time);
    EXPECT_EQ(1, results1.size());
    EXPECT_DOUBLE_EQ(2, results1[0]);
}

TEST_F(ConcentrationMeasurementTest, PerformNormalPeriodTwoFilaments) {
    measurements::Concentration m(one, 0.5);

    m.initialize(filaments, concentrations);

    // Measure before the next sample period
    m.perform(0.4, filaments, concentrations);

    std::vector<double> results1(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(1, results1.size());
    EXPECT_DOUBLE_EQ(2, results1[0]);

    concentrations[one]->add_monomer();
    m.perform(0.7, filaments, concentrations);

    std::vector<double> results2(m.get_means());

    EXPECT_DOUBLE_EQ(0.5, m.previous_time);
    EXPECT_EQ(2, results2.size());
    EXPECT_DOUBLE_EQ(2,   results2[0]);
    EXPECT_DOUBLE_EQ(2.5, results2[1]);

    // Skip multiple sample periods

    concentrations[one]->add_monomer();
    m.perform(1.7, filaments, concentrations);

    std::vector<double> results3(m.get_means());

    EXPECT_DOUBLE_EQ(1.5, m.previous_time);
    EXPECT_EQ(4, results3.size());
    EXPECT_DOUBLE_EQ(2,   results3[0]);
    EXPECT_DOUBLE_EQ(2.5, results3[1]);
    EXPECT_DOUBLE_EQ(3,   results3[2]);
    EXPECT_DOUBLE_EQ(3,   results3[3]);

    // check edge case (time exactly on sample)
    concentrations[one]->add_monomer();
    m.perform(1.7, filaments, concentrations);
    m.perform(2, filaments, concentrations);

    std::vector<double> results4(m.get_means());

    EXPECT_DOUBLE_EQ(2, m.previous_time);
    EXPECT_EQ(5, results4.size());
    EXPECT_DOUBLE_EQ(2,   results4[0]);
    EXPECT_DOUBLE_EQ(2.5, results4[1]);
    EXPECT_DOUBLE_EQ(3,   results4[2]);
    EXPECT_DOUBLE_EQ(3,   results4[3]);
    EXPECT_DOUBLE_EQ(3.5, results4[4]);
}

TEST_F(ConcentrationMeasurementTest, PerformNormalPeriod) {
    measurements::Concentration m(zero, 0.5);

    m.initialize(filaments, concentrations);

    // Measure before the next sample period
    m.perform(0.4, filaments, concentrations);

    std::vector<double> results1(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(1, results1.size());
    EXPECT_DOUBLE_EQ(4, results1[0]);

    concentrations[zero]->add_monomer();
    m.perform(0.7, filaments, concentrations);

    std::vector<double> results2(m.get_means());

    EXPECT_DOUBLE_EQ(0.5, m.previous_time);
    EXPECT_EQ(2, results2.size());
    EXPECT_DOUBLE_EQ(4, results2[0]);
    EXPECT_DOUBLE_EQ(5, results2[1]);

    // Skip multiple sample periods

    concentrations[zero]->add_monomer();
    m.perform(1.7, filaments, concentrations);

    std::vector<double> results3(m.get_means());

    EXPECT_DOUBLE_EQ(1.5, m.previous_time);
    EXPECT_EQ(4, results3.size());
    EXPECT_DOUBLE_EQ(4, results3[0]);
    EXPECT_DOUBLE_EQ(5, results3[1]);
    EXPECT_DOUBLE_EQ(6, results3[2]);
    EXPECT_DOUBLE_EQ(6, results3[3]);

    // check edge case (time exactly on sample)
    concentrations[zero]->add_monomer();
    m.perform(1.7, filaments, concentrations);
    m.perform(2, filaments, concentrations);

    std::vector<double> results4(m.get_means());

    EXPECT_DOUBLE_EQ(2, m.previous_time);
    EXPECT_EQ(5, results4.size());
    EXPECT_DOUBLE_EQ(4, results4[0]);
    EXPECT_DOUBLE_EQ(5, results4[1]);
    EXPECT_DOUBLE_EQ(6, results4[2]);
    EXPECT_DOUBLE_EQ(6, results4[3]);
    EXPECT_DOUBLE_EQ(7, results4[4]);
}

TEST_F(ConcentrationMeasurementTest, PerformZeroPeriod) {
    measurements::Concentration m(zero, 0);

    m.initialize(filaments, concentrations);

    m.perform(0.1, filaments, concentrations);

    std::vector<double> results(m.get_means());

    EXPECT_EQ(0, m.previous_time);

    EXPECT_EQ(2, results.size());
    EXPECT_DOUBLE_EQ(4, results[0]);
    EXPECT_DOUBLE_EQ(4, results[1]);
}
