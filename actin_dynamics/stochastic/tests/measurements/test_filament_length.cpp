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
#include "filaments/simple_filament.h"
#include "measurements/filament_length.h"

using namespace stochastic;

class FilamentLengthTest : public testing::Test {
    protected:
        virtual void SetUp() {
            std::vector<State> values1;
            values1 += zero, one, zero, zero, two, one, zero, one;
            std::vector<State> values2;
            values2 += one, one, two, zero, two, zero, zero, one;

            filaments.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values1)));
            filaments.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values2)));
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(FilamentLengthTest, Initialize) {
    measurements::FilamentLength m(0);

    m.initialize(filaments, concentrations);

    measurements::length_vector_t results(m.get_values());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(2, results.size());
    EXPECT_EQ(1, results[0].size());
    EXPECT_EQ(8, results[0][0]);
    EXPECT_EQ(1, results[1].size());
    EXPECT_EQ(8, results[1][0]);
}

TEST_F(FilamentLengthTest, PerformNormalPeriod) {
    measurements::FilamentLength m(0.5);

    m.initialize(filaments, concentrations);

    // Measure before the next sample period
    m.perform(0.4, filaments, concentrations);

    measurements::length_vector_t results1(m.get_values());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(2, results1.size());
    EXPECT_EQ(1, results1[0].size());
    EXPECT_EQ(8, results1[0][0]);
    EXPECT_EQ(1, results1[1].size());
    EXPECT_EQ(8, results1[1][0]);

    m.perform(0.7, filaments, concentrations);

    measurements::length_vector_t results2(m.get_values());

    EXPECT_DOUBLE_EQ(0.5, m.previous_time);
    EXPECT_EQ(2, results2.size());
    EXPECT_EQ(2, results2[0].size());
    EXPECT_EQ(8, results2[0][1]);
    EXPECT_EQ(2, results2[1].size());
    EXPECT_EQ(8, results2[1][1]);

    // Skip multiple sample periods
    m.perform(1.7, filaments, concentrations);

    measurements::length_vector_t results3(m.get_values());

    EXPECT_DOUBLE_EQ(1.5, m.previous_time);
    EXPECT_EQ(2, results3.size());
    EXPECT_EQ(4, results3[0].size());
    EXPECT_EQ(8, results3[0][1]);
    EXPECT_EQ(4, results3[1].size());
    EXPECT_EQ(8, results3[1][1]);


    // check edge case (time exactly on sample)
    m.perform(2, filaments, concentrations);

    measurements::length_vector_t results4(m.get_values());

    EXPECT_DOUBLE_EQ(2, m.previous_time);
    EXPECT_EQ(2, results4.size());
    EXPECT_EQ(5, results4[0].size());
    EXPECT_EQ(8, results4[0][1]);
    EXPECT_EQ(5, results4[1].size());
    EXPECT_EQ(8, results4[1][1]);
}

TEST_F(FilamentLengthTest, PerformZeroPeriod) {
    measurements::FilamentLength m(0);

    m.initialize(filaments, concentrations);

    m.perform(0.1, filaments, concentrations);

    measurements::length_vector_t results1(m.get_values());

    EXPECT_EQ(0, m.previous_time);

    EXPECT_EQ(2, results1.size());
    EXPECT_EQ(2, results1[0].size());
    EXPECT_EQ(8, results1[0][1]);
    EXPECT_EQ(2, results1[1].size());
    EXPECT_EQ(8, results1[1][1]);
}
