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
#include <boost/shared_ptr.hpp>

// Bring operator+= into the namespace
using namespace boost::assign;

#include "state.h"

#include "transitions/vectorial_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

class VectorialHydrolysisTest : public testing::Test {
    protected:
        virtual void SetUp() {
            std::vector<State> values1;
            values1 += 0, 1, 0, 0, 2, 1, 0, 1;
            std::vector<State> values2;
            values2 += 1, 1, 2, 0, 2, 0, 0, 0;

            filaments.push_back(filament_ptr_t(new SimpleFilament(values1)));
            filaments.push_back(filament_ptr_t(new SimpleFilament(values2)));

            concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 1)));
            concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 1)));
            concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 1)));
            concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 1)));
            concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 1)));
        }
        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filament_container_t filaments;
        concentration_container_t concentrations;
};

TEST_F(VectorialHydrolysisTest, initial_R) {
    VectorialHydrolysis t_01_2(0, 1, 2, 3);
    VectorialHydrolysis t_02_3(0, 2, 3, 4);
    VectorialHydrolysis t_12_3(1, 2, 3, 5);
    VectorialHydrolysis t_21_3(2, 1, 3, 6);

    EXPECT_DOUBLE_EQ(6, t_01_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(8, t_02_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(5, t_12_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_21_3.initial_R(0, filaments, concentrations));
}

TEST_F(VectorialHydrolysisTest, Perform) {
    VectorialHydrolysis t_01_2(0, 1, 2, 3);
    VectorialHydrolysis t_02_3(0, 2, 3, 4);
    VectorialHydrolysis t_12_3(1, 2, 3, 5);
    VectorialHydrolysis t_21_3(2, 1, 3, 6);

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
    VectorialHydrolysisWithByproduct t_01_2(0, 1, 2, 3, 4);
    VectorialHydrolysisWithByproduct t_02_3(0, 2, 3, 4, 4);
    VectorialHydrolysisWithByproduct t_12_3(1, 2, 3, 5, 4);
    VectorialHydrolysisWithByproduct t_21_3(2, 1, 3, 6, 4);

    EXPECT_DOUBLE_EQ(6, t_01_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(8, t_02_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(5, t_12_3.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_21_3.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, t_01_2.perform(0, 1.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(12, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 6, t_21_3.R(0, filaments, concentrations, 0));
    EXPECT_EQ(1, concentrations[4]->monomer_count());

    EXPECT_EQ(0, t_02_3.perform(0, 5.3, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 3, t_01_2.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 8, t_02_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 5, t_12_3.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_21_3.R(0, filaments, concentrations, 0));
    EXPECT_EQ(2, concentrations[4]->monomer_count());
}
