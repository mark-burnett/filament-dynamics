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

#include "transitions/vectorial_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class VectorialHydrolysisTest : public testing::Test {
    protected:
        VectorialHydrolysisTest() :
            t_01_2(zero, one, two, 3),
            t_02_3(zero, two, three, 4),
            t_12_3(one, two, three, 5),
            t_21_3(two, one, three, 6) {}

        virtual void SetUp() {
            std::vector<State> values1;
            values1 += zero, one, zero, zero, two, one, zero, one;
            std::vector<State> values2;
            values2 += one, one, two, zero, two, zero, zero, zero;

            filaments.push_back(filaments::base_ptr_t(
                        new filaments::SimpleFilament(values1)));
            filaments.push_back(filaments::base_ptr_t(
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
            filaments.clear();
            concentrations.clear();
        }

        transitions::VectorialHydrolysis t_01_2;
        transitions::VectorialHydrolysis t_02_3;
        transitions::VectorialHydrolysis t_12_3;
        transitions::VectorialHydrolysis t_21_3;

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(VectorialHydrolysisTest, initial_R) {
    EXPECT_DOUBLE_EQ(6, t_01_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(8, t_02_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(5, t_12_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_21_3.initial_R(0, filaments, concentrations));
}

TEST_F(VectorialHydrolysisTest, Perform) {
    EXPECT_DOUBLE_EQ(6, t_01_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(8, t_02_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(5, t_12_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_21_3.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, t_01_2.perform(0, 1.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(12, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 6, t_21_3.R(0, filaments, concentrations, 0));

    EXPECT_EQ(0, t_02_3.perform(0, 5.3, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 8, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_21_3.R(0, filaments, concentrations, 0));
}

TEST_F(VectorialHydrolysisTest, ByproductPerform) {
    transitions::VectorialHydrolysisWithByproduct t_01_2(zero, one, two, 3, four);
    transitions::VectorialHydrolysisWithByproduct t_02_3(zero, two, three, 4, four);
    transitions::VectorialHydrolysisWithByproduct t_12_3(one, two, three, 5, four);
    transitions::VectorialHydrolysisWithByproduct t_21_3(two, one, three, 6, four);

    EXPECT_DOUBLE_EQ(6, t_01_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(8, t_02_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(5, t_12_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_21_3.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, t_01_2.perform(0, 1.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(12, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 6, t_21_3.R(0, filaments, concentrations, 0));
    EXPECT_EQ(1, concentrations[four]->monomer_count());

    EXPECT_EQ(0, t_02_3.perform(0, 5.3, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 8, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_21_3.R(0, filaments, concentrations, 0));
    EXPECT_EQ(2, concentrations[four]->monomer_count());
}
