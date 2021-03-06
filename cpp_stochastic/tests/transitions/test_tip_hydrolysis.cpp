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

#include "transitions/tip_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class TipHydrolysisTest : public testing::Test {
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
                        new concentrations::FixedReagent(0, 1));
        }

        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};

TEST_F(TipHydrolysisTest, BETipHydrolysis) {
    transitions::BarbedTipHydrolysis be_10(one, zero, 3);
    transitions::BarbedTipHydrolysis be_01(zero, one, 2);

    EXPECT_DOUBLE_EQ(3, be_10.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(2, be_01.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, be_10.perform(0, 0.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(0, be_10.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(4, be_01.R(0, filaments, concentrations, 0));

    EXPECT_EQ(1, be_01.perform(0, 2.7, filaments, concentrations));
    EXPECT_DOUBLE_EQ(3, be_10.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(2, be_01.R(0, filaments, concentrations, 1));

}

TEST_F(TipHydrolysisTest, PETipHydrolysis) {
    transitions::PointedTipHydrolysis pe_12(one, two, 3);

    EXPECT_DOUBLE_EQ(3, pe_12.initial_R(0, filaments, concentrations));
    EXPECT_EQ(1, pe_12.perform(0, 0.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(0, pe_12.R(0, filaments, concentrations, 1));
}

TEST_F(TipHydrolysisTest, BETipHydrolysisWB) {
    transitions::BarbedTipHydrolysisWithByproduct be_12(one, two, 3, three);

    EXPECT_DOUBLE_EQ(3, be_12.initial_R(0, filaments, concentrations));
    EXPECT_EQ(0, be_12.perform(0, 0.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(0, be_12.R(0, filaments, concentrations, 0));
    EXPECT_EQ(1, concentrations[three]->monomer_count());
}

TEST_F(TipHydrolysisTest, PETipHydrolysisWB) {
    transitions::PointedTipHydrolysisWithByproduct pe_12(one, two, 3, three);

    EXPECT_DOUBLE_EQ(3, pe_12.initial_R(0, filaments, concentrations));
    EXPECT_EQ(1, pe_12.perform(0, 0.2, filaments, concentrations));
    EXPECT_DOUBLE_EQ(0, pe_12.R(0, filaments, concentrations, 1));
    EXPECT_EQ(1, concentrations[three]->monomer_count());
}
