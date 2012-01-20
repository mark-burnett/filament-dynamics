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

            filaments2.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values1)));
            filaments2.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values2)));
        }

        filaments::container_t filaments;
        filaments::container_t filaments2;
        concentrations::container_t concentrations;
};

TEST_F(FilamentLengthTest, TwoFilaments) {
    measurements::FilamentLength m(0);

    m.initialize(filaments2, concentrations);

    std::vector<double> results1(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(1, results1.size());
    EXPECT_EQ(8, results1[0]);

    filaments2[0]->append_barbed(one);
    m.perform(0.1, filaments2, concentrations);
    std::vector<double> results2(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(2, results2.size());
    EXPECT_DOUBLE_EQ(8,   results2[0]);
    EXPECT_DOUBLE_EQ(8.5, results2[1]);

    filaments2[0]->append_barbed(one);
    m.perform(0.1, filaments2, concentrations);
    std::vector<double> results3(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(3, results3.size());
    EXPECT_DOUBLE_EQ(8,   results3[0]);
    EXPECT_DOUBLE_EQ(8.5, results3[1]);
    EXPECT_DOUBLE_EQ(9,   results3[2]);

    filaments2[1]->pop_barbed();
    m.perform(0.1, filaments2, concentrations);
    std::vector<double> results4(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(4, results4.size());
    EXPECT_DOUBLE_EQ(8,   results4[0]);
    EXPECT_DOUBLE_EQ(8.5, results4[1]);
    EXPECT_DOUBLE_EQ(9,   results4[2]);
    EXPECT_DOUBLE_EQ(8.5, results4[3]);

    filaments2[1]->pop_barbed();
    m.perform(0.1, filaments2, concentrations);
    std::vector<double> results5(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(5, results5.size());
    EXPECT_DOUBLE_EQ(8,   results5[0]);
    EXPECT_DOUBLE_EQ(8.5, results5[1]);
    EXPECT_DOUBLE_EQ(9,   results5[2]);
    EXPECT_DOUBLE_EQ(8.5, results5[3]);
    EXPECT_DOUBLE_EQ(8,   results5[4]);
}

TEST_F(FilamentLengthTest, Initialize) {
    measurements::FilamentLength m(0);

    m.initialize(filaments, concentrations);

    std::vector<double> results(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(1, results.size());
    EXPECT_EQ(8, results[0]);
}

TEST_F(FilamentLengthTest, PerformNormalPeriod) {
    measurements::FilamentLength m(0.5);

    m.initialize(filaments, concentrations);

    // Measure before the next sample period
    m.perform(0.4, filaments, concentrations);

    std::vector<double> results1(m.get_means());

    EXPECT_EQ(0, m.previous_time);
    EXPECT_EQ(1, results1.size());
    EXPECT_EQ(8, results1[0]);

    filaments[0]->append_barbed(one);
    m.perform(0.7, filaments, concentrations);

    std::vector<double> results2(m.get_means());

    EXPECT_DOUBLE_EQ(0.5, m.previous_time);
    EXPECT_EQ(2, results2.size());
    EXPECT_EQ(8, results2[0]);
    EXPECT_EQ(9, results2[1]);

    // Skip multiple sample periods
    filaments[0]->append_barbed(one);
    m.perform(1.7, filaments, concentrations);

    std::vector<double> results3(m.get_means());

    EXPECT_DOUBLE_EQ(1.5, m.previous_time);
    EXPECT_EQ( 4, results3.size());
    EXPECT_EQ( 8, results3[0]);
    EXPECT_EQ( 9, results3[1]);
    EXPECT_EQ(10, results3[2]);
    EXPECT_EQ(10, results3[3]);


    // check edge case (time exactly on sample)
    filaments[0]->append_barbed(one);
    m.perform(2, filaments, concentrations);

    std::vector<double> results4(m.get_means());

    EXPECT_DOUBLE_EQ(2, m.previous_time);
    EXPECT_EQ( 5, results4.size());
    EXPECT_EQ( 8, results4[0]);
    EXPECT_EQ( 9, results4[1]);
    EXPECT_EQ(10, results4[2]);
    EXPECT_EQ(10, results4[3]);
    EXPECT_EQ(11, results4[4]);
}

TEST_F(FilamentLengthTest, PerformZeroPeriod) {
    measurements::FilamentLength m(0);

    m.initialize(filaments, concentrations);

    m.perform(0.1, filaments, concentrations);

    std::vector<double> results(m.get_means());

    EXPECT_EQ(0, m.previous_time);

    EXPECT_EQ(2, results.size());
    EXPECT_EQ(8, results[0]);
    EXPECT_EQ(8, results[1]);
}
