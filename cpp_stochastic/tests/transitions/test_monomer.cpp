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

#include "state.h"

#include "test_states.h"

#include "transitions/monomer.h"
#include "concentrations/fixed_reagent.h"
#include "filaments/filament.h"

using namespace stochastic;

class MonomerTest : public testing::Test {
    protected:
        virtual void SetUp() {
            concentrations[zero] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(8, 0.5));
            concentrations[one] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(6, 0.5));
            concentrations[two] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(4, 0.5));
            concentrations[three] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(2, 0.5));
        }

        virtual void TearDown() {
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(MonomerTest, Initial_R) {
    transitions::Monomer a_01(zero, one, 3);
    transitions::Monomer a_12(one, two, 1.5);

    EXPECT_DOUBLE_EQ(48,  a_01.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(18, a_12.initial_R(0, filaments, concentrations));
}

TEST_F(MonomerTest, Perform) {
    transitions::Monomer a_01(zero, one, 3);
    transitions::Monomer a_12(one, two, 1.5);

    EXPECT_DOUBLE_EQ(48, a_01.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(18, a_12.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, a_01.perform(0, 1000, filaments, concentrations));

    EXPECT_EQ(15, concentrations[zero]->monomer_count());
    EXPECT_EQ(13, concentrations[one]->monomer_count());
    EXPECT_DOUBLE_EQ(45,   a_01.R(0, filaments, concentrations, 1000));
    EXPECT_DOUBLE_EQ(19.5, a_12.R(0, filaments, concentrations, 1000));
}

TEST_F(MonomerTest, PerformWithByproduct) {
    transitions::MonomerWithByproduct a_01(zero, one, 3, three);
    transitions::MonomerWithByproduct a_12(one, two, 1.5, three);

    EXPECT_DOUBLE_EQ(48, a_01.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(18, a_12.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, a_01.perform(0, 1000, filaments, concentrations));

    EXPECT_EQ(15, concentrations[zero]->monomer_count());
    EXPECT_EQ(13, concentrations[one]->monomer_count());
    EXPECT_EQ(5,  concentrations[three]->monomer_count());
    EXPECT_DOUBLE_EQ(45,   a_01.R(0, filaments, concentrations, 1000));
    EXPECT_DOUBLE_EQ(19.5, a_12.R(0, filaments, concentrations, 1000));
}
