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

#include "transitions/association.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class AssociationTest : public testing::Test {
    protected:
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
                        new concentrations::FixedReagent(4, 1));
        }

        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(AssociationTest, initial_R) {
    transitions::Association a_3_12(three, one, two, 3);
    transitions::Association a_3_01(three, zero, one, 2);

    EXPECT_DOUBLE_EQ(60, a_3_12.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(64, a_3_01.initial_R(0, filaments, concentrations));
}

TEST_F(AssociationTest, perform) {
    transitions::Association a_3_12(three, one, two, 3);
    transitions::Association a_3_01(three, zero, one, 2);

    EXPECT_DOUBLE_EQ(60, a_3_12.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(64, a_3_01.initial_R(0, filaments, concentrations));

    EXPECT_EQ(1, a_3_12.perform(0, 41, filaments, concentrations));
    EXPECT_DOUBLE_EQ(36, a_3_12.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(48, a_3_01.R(0, filaments, concentrations, 1));
    EXPECT_EQ(3, concentrations[three]->monomer_count());
}
