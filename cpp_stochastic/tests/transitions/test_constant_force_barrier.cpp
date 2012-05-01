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

#include "transitions/constant_force_barrier.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class RaiseBarrierConstantForceTest : public testing::Test {
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

TEST_F(RaiseBarrierConstantForceTest, initial_R) {
    transitions::RaiseBarrierConstantForce rb(3.0e-12, 1.0e-14, 10);
    EXPECT_DOUBLE_EQ(124112.29999557146,
            rb.initial_R(0, filaments, concentrations));
}

TEST_F(RaiseBarrierConstantForceTest, R) {
    transitions::RaiseBarrierConstantForce rb(3.0e-12, 1.0e-14, 10);

    EXPECT_DOUBLE_EQ(124112.29999557146,
            rb.R(0, filaments, concentrations, 0));
}

TEST_F(RaiseBarrierConstantForceTest, perform) {
    transitions::RaiseBarrierConstantForce rb(3.0e-6, 0.01, 10);
    barrier_position = 0;

    EXPECT_EQ(0, rb.perform(0, -1, filaments, concentrations));
    EXPECT_EQ(1, barrier_position);
}

class LowerBarrierConstantForceTest : public testing::Test {
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

TEST_F(LowerBarrierConstantForceTest, initial_R) {
    transitions::LowerBarrierConstantForce lb(3.0e-12, 1.0e-14, 10);
    EXPECT_DOUBLE_EQ(151610.79306612333,
            lb.initial_R(0, filaments, concentrations));
    EXPECT_EQ(81, barrier_position);
}

TEST_F(LowerBarrierConstantForceTest, R) {
    transitions::LowerBarrierConstantForce lb(3.0e-12, 1.0e-14, 10);
    EXPECT_DOUBLE_EQ(151610.79306612333,
            lb.initial_R(0, filaments, concentrations));
    EXPECT_EQ(81, barrier_position);

    EXPECT_DOUBLE_EQ(151610.79306612333,
            lb.R(0, filaments, concentrations, 0));
}

TEST_F(LowerBarrierConstantForceTest, perform) {
    transitions::LowerBarrierConstantForce lb(3.0e-12, 1.0e-14, 10);
    EXPECT_DOUBLE_EQ(151610.79306612333,
            lb.initial_R(0, filaments, concentrations));
    EXPECT_EQ(81, barrier_position);

    EXPECT_EQ(0, lb.perform(0, -1, filaments, concentrations));
    EXPECT_EQ(80, barrier_position);
    EXPECT_DOUBLE_EQ(0, lb.R(0, filaments, concentrations, 0));
}
