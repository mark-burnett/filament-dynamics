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

#include "transitions/polymerization.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

using namespace stochastic;

class Polymerization : public testing::Test {
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
                        new concentrations::FixedReagent(6, 1));
            concentrations[1] = concentrations::Concentration::ptr_t(
                        new concentrations::FixedReagent(4, 1));
        }

        virtual void TearDown() {
            filaments.clear();
            concentrations.clear();
        }

        filaments::container_t filaments;
        concentrations::container_t concentrations;
};


TEST_F(Polymerization, Basic) {
    transitions::BarbedEndPolymerization t_b0(0, 1);
    transitions::BarbedEndPolymerization t_b1(1, 2);
    transitions::PointedEndPolymerization t_p0(0, 3);
    transitions::PointedEndPolymerization t_p1(1, 4);

    EXPECT_DOUBLE_EQ(12, t_b0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(16, t_b1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(36, t_p0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(32, t_p1.initial_R(0, filaments, concentrations));
    EXPECT_EQ(6, concentrations[0]->monomer_count());
    EXPECT_EQ(4, concentrations[1]->monomer_count());

    EXPECT_EQ(1, t_b0.perform(0, 8.5, filaments, concentrations));
    EXPECT_EQ(8, filaments[0]->length());
    EXPECT_EQ(9, filaments[1]->length());
    EXPECT_EQ(0, filaments[1]->barbed_state());
    EXPECT_DOUBLE_EQ(10, t_b0.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(16, t_b1.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(30, t_p0.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(32, t_p1.R(0, filaments, concentrations, 1));
    EXPECT_EQ(5, concentrations[0]->monomer_count());
    EXPECT_EQ(4, concentrations[1]->monomer_count());

    EXPECT_EQ(0, t_p1.perform(0, 12.1, filaments, concentrations));
    EXPECT_EQ(9, filaments[0]->length());
    EXPECT_EQ(9, filaments[1]->length());
    EXPECT_EQ(1, filaments[0]->pointed_state());
    EXPECT_DOUBLE_EQ(10, t_b0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(12, t_b1.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(30, t_p0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(24, t_p1.R(0, filaments, concentrations, 0));
    EXPECT_EQ(5, concentrations[0]->monomer_count());
    EXPECT_EQ(3, concentrations[1]->monomer_count());

}

TEST_F(Polymerization, DisableTime) {
    transitions::BarbedEndPolymerization t_b0(0, 1, 4);
    transitions::BarbedEndPolymerization t_b1(1, 2, 3);
    transitions::PointedEndPolymerization t_p0(0, 3, 2);
    transitions::PointedEndPolymerization t_p1(1, 4, 1);

    EXPECT_DOUBLE_EQ(12, t_b0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(16, t_b1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(36, t_p0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(32, t_p1.initial_R(0, filaments, concentrations));

    EXPECT_DOUBLE_EQ(12, t_b0.R(1, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(16, t_b1.R(1, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(36, t_p0.R(1, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(32, t_p1.R(1, filaments, concentrations, 0));

    EXPECT_DOUBLE_EQ(12, t_b0.R(2, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(16, t_b1.R(2, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(36, t_p0.R(2, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p1.R(2, filaments, concentrations, 0));

    EXPECT_DOUBLE_EQ(12, t_b0.R(3, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(16, t_b1.R(3, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p0.R(3, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p1.R(3, filaments, concentrations, 0));

    EXPECT_DOUBLE_EQ(12, t_b0.R(4, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_b1.R(4, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p0.R(4, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p1.R(4, filaments, concentrations, 0));

    EXPECT_DOUBLE_EQ( 0, t_b0.R(5, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_b1.R(5, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p0.R(5, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 0, t_p1.R(5, filaments, concentrations, 0));
}
