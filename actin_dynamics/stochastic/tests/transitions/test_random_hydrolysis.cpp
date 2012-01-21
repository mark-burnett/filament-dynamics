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

#include "state.h"

#include "test_states.h"

#include "transitions/random_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class RandomHydrolysisTest : public testing::Test {
    protected:
        virtual void SetUp() {
            std::vector<State> values1;
            values1 += zero, one, zero, zero, two, one, zero, one;
            std::vector<State> values2;
            values2 += one, one, two, zero, two, zero, zero, one;

            one_filament.push_back(filaments::Filament::ptr_t(
                        new filaments::SimpleFilament(values1)));

            two_filaments.push_back(filaments::Filament::ptr_t(
                        new filaments::SimpleFilament(values1)));
            two_filaments.push_back(filaments::Filament::ptr_t(
                        new filaments::SimpleFilament(values2)));

            concentrations[zero] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[one] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[two] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[three] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[four] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
        }

        virtual void TearDown() {
            one_filament.clear();
            two_filaments.clear();
            concentrations.clear();
        }

        filaments::container_t one_filament;
        filaments::container_t two_filaments;
        concentrations::container_t concentrations;
};

TEST_F(RandomHydrolysisTest, SingleFilamentR) {
    transitions::RandomHydrolysis t_0(zero, four, 3);
    transitions::RandomHydrolysis t_1(one, four, 2);
    transitions::RandomHydrolysis t_2(two, four, 4);
    transitions::RandomHydrolysis t_3(three, four, 9);

    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_1.initial_R(0, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 4, t_2.initial_R(0, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 0, t_3.initial_R(0, one_filament, concentrations));
}

TEST_F(RandomHydrolysisTest, DoubleFilamentR) {
    transitions::RandomHydrolysis t_0(zero, four, 3);
    transitions::RandomHydrolysis t_1(one, four, 2);
    transitions::RandomHydrolysis t_2(two, four, 4);
    transitions::RandomHydrolysis t_3(three, four, 9);

    EXPECT_DOUBLE_EQ(21, t_0.initial_R(0, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_1.initial_R(0, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_2.initial_R(0, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ( 0, t_3.initial_R(0, two_filaments, concentrations));
}

TEST_F(RandomHydrolysisTest, SingleFilamentPerform) {
    transitions::RandomHydrolysis t_0(zero, one, 3);
    transitions::RandomHydrolysis t_1(one, two, 2);
    transitions::RandomHydrolysis t_2(two, four, 4);

    // Must call R before perform
    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_1.initial_R(0, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 4, t_2.initial_R(0, one_filament, concentrations));

    EXPECT_EQ(0, t_0.perform(0, 2.1, one_filament, concentrations));
    EXPECT_DOUBLE_EQ(9, t_0.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_1.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ(4, t_2.R(0, one_filament, concentrations, 0));
    EXPECT_EQ(one, one_filament[0]->pointed_state());

    EXPECT_EQ(0, t_0.perform(0, 8, one_filament, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_0.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ(10, t_1.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ( 4, t_2.R(0, one_filament, concentrations, 0));
    EXPECT_EQ(one, one_filament[0]->barbed_state());

    EXPECT_EQ(0, t_1.perform(0, 9, one_filament, concentrations));
    EXPECT_DOUBLE_EQ(6, t_0.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_1.R(0, one_filament, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_2.R(0, one_filament, concentrations, 0));
    EXPECT_EQ(two, one_filament[0]->barbed_state());
}

TEST_F(RandomHydrolysisTest, DoubleFilamentPerform) {
    transitions::RandomHydrolysis t_0(zero, one, 3);
    transitions::RandomHydrolysis t_1(one, two, 2);
    transitions::RandomHydrolysis t_2(two, three, 4);


    // Must call R before perform
    EXPECT_DOUBLE_EQ(21, t_0.initial_R(0, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_1.initial_R(0, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_2.initial_R(0, two_filaments, concentrations));

    EXPECT_EQ(1, t_1.perform(0, 7, two_filaments, concentrations));
    EXPECT_DOUBLE_EQ(21, t_0.R(0, two_filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(10, t_1.R(0, two_filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(16, t_2.R(0, two_filaments, concentrations, 1));
    EXPECT_EQ(two, two_filaments[1]->pointed_state());
}

TEST_F(RandomHydrolysisTest, WithByproductPerform) {
    transitions::RandomHydrolysisWithByproduct t_0(zero, one, 3, zero);

    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, one_filament, concentrations));

    EXPECT_EQ(0, t_0.perform(0, 1, one_filament, concentrations));
    EXPECT_DOUBLE_EQ(9, t_0.R(0, one_filament, concentrations, 0));
    EXPECT_EQ(1, concentrations[zero]->monomer_count());
}
