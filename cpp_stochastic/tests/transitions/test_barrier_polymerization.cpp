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

#include "transitions/barrier_polymerization.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

#include "barrier_position.h"

using namespace stochastic;

class StepFunctionBarrierPolymerizationTest : public testing::Test {
    protected:
        virtual void SetUp() {
            std::vector<State> values1;
            values1 += zero, one, zero, zero, two, one, zero, one;
            std::vector<State> values2;
            values2 += one, one, two, zero, two, zero, zero, zero;

            filaments.push_back(filaments::Filament::ptr_t(
                        new filaments::SimpleFilament(values1)));
            filaments.push_back(filaments::Filament::ptr_t(
                        new filaments::SimpleFilament(values2)));

            concentrations[zero] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[one] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[two] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(0, 1));
            concentrations[three] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(4, 1));
        }

        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(StepFunctionBarrierPolymerizationTest, initial_R) {
    transitions::StepFunctionBarrierBarbedEndPolymerization p0(zero, 3, 100);

    barrier_position = 0;
    EXPECT_DOUBLE_EQ(0, p0.initial_R(0, filaments, concentrations));
    barrier_position = 10000;
    EXPECT_DOUBLE_EQ(6, p0.initial_R(0, filaments, concentrations));

    barrier_position = 899;
    EXPECT_DOUBLE_EQ(0, p0.initial_R(0, filaments, concentrations));
    barrier_position = 900;
    EXPECT_DOUBLE_EQ(6, p0.initial_R(0, filaments, concentrations));
    barrier_position = 901;
    EXPECT_DOUBLE_EQ(6, p0.initial_R(0, filaments, concentrations));
}

TEST_F(StepFunctionBarrierPolymerizationTest, R) {
    transitions::StepFunctionBarrierBarbedEndPolymerization p0(zero, 3, 100);

    barrier_position = 0;
    EXPECT_DOUBLE_EQ(0, p0.R(0, filaments, concentrations, 0));
    barrier_position = 10000;
    EXPECT_DOUBLE_EQ(6, p0.R(0, filaments, concentrations, 0));

    barrier_position = 899;
    EXPECT_DOUBLE_EQ(0, p0.R(0, filaments, concentrations, 0));
    barrier_position = 900;
    EXPECT_DOUBLE_EQ(6, p0.R(0, filaments, concentrations, 0));
    barrier_position = 901;
    EXPECT_DOUBLE_EQ(6, p0.R(0, filaments, concentrations, 0));
}

TEST_F(StepFunctionBarrierPolymerizationTest, perform) {
    transitions::StepFunctionBarrierBarbedEndPolymerization p0(zero, 3, 100);

    barrier_position = 999;
    EXPECT_DOUBLE_EQ(6, p0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(0, p0.perform(0, 2.1, filaments, concentrations));
    EXPECT_DOUBLE_EQ(3, p0.R(0, filaments, concentrations, 0));

    barrier_position = 1000;
    EXPECT_DOUBLE_EQ(6, p0.R(0, filaments, concentrations, 0));
}
