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

#include "transitions/cooperative_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class CooperativeHydrolysisTest : public testing::Test {
    protected:
        virtual void SetUp() {
            std::vector<State> values1;
            values1 += 0, 1, 0, 0, 2, 1, 0, 1;
            std::vector<State> values2;
            values2 += 1, 1, 2, 0, 2, 0, 0, 0;

            filaments.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values1)));
            filaments.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values2)));

            concentrations[0] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[1] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[2] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[3] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[4] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
        }
        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(CooperativeHydrolysisTest, RandomEquivalence) {
    transitions::CooperativeHydrolysis tr_12(0, 1, 2, 3);

    EXPECT_DOUBLE_EQ(15, tr_12.initial_R(0, filaments, concentrations));
    EXPECT_EQ(1, tr_12.perform(0, 14.1, filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, tr_12.R(0, filaments, concentrations, 1));
}

TEST_F(CooperativeHydrolysisTest, Mixed) {
    transitions::CooperativeHydrolysis t01_2(0, 1, 2, 3, 11);

    EXPECT_DOUBLE_EQ(75, t01_2.initial_R(0, filaments, concentrations));

    // Random Transition - no effect on boundaries
    EXPECT_EQ(1, t01_2.perform(0, 11.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(72, t01_2.R(0, filaments, concentrations, 1));

    // Vectorial Transition - subtracts (30 + 3 from Rate)
    EXPECT_EQ(0, t01_2.perform(0, 43, filaments, concentrations));
    EXPECT_DOUBLE_EQ(39, t01_2.R(0, filaments, concentrations, 0));
}

TEST_F(CooperativeHydrolysisTest, MixedWithByproduct) {
    transitions::CooperativeHydrolysisWithByproduct t01_2_3(0, 1, 2, 3, 3, 11);

    EXPECT_DOUBLE_EQ(75, t01_2_3.initial_R(0, filaments, concentrations));

    // Random Transition - no effect on boundaries
    EXPECT_EQ(1, t01_2_3.perform(0, 11.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(72, t01_2_3.R(0, filaments, concentrations, 1));
    EXPECT_EQ(1, concentrations[3]->monomer_count());

    // Vectorial Transition - subtracts (30 + 3 from Rate)
    EXPECT_EQ(0, t01_2_3.perform(0, 43, filaments, concentrations));
    EXPECT_DOUBLE_EQ(39, t01_2_3.R(0, filaments, concentrations, 0));
    EXPECT_EQ(2, concentrations[3]->monomer_count());
}
