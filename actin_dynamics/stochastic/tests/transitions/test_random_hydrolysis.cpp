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

#include "transitions/random_hydrolysis.h"
#include "filaments/simple_filament.h"
#include "concentrations/fixed_reagent.h"

TEST(RandomHydrolysis, SingleFilamentR) {
    std::vector<State> values;
    values += 0, 1, 0, 0, 2, 1, 0, 1;

    filament_container_t filaments;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values.begin(), values.end())));

    concentration_container_t concentrations;

    RandomHydrolysis t_0(0, 7, 3);
    RandomHydrolysis t_1(1, 7, 2);
    RandomHydrolysis t_2(2, 7, 4);
    RandomHydrolysis t_3(3, 7, 9);

    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 4, t_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 0, t_3.initial_R(0, filaments, concentrations));
}

TEST(RandomHydrolysis, DoubleFilamentR) {
    std::vector<State> values1;
    values1 += 0, 1, 0, 0, 2, 1, 0, 1;
    std::vector<State> values2;
    values2 += 1, 1, 2, 0, 2, 0, 0, 1;

    filament_container_t filaments;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values1.begin(), values1.end())));
    filaments.push_back(filament_ptr_t(new SimpleFilament(values2.begin(), values2.end())));

    concentration_container_t concentrations;

    RandomHydrolysis t_0(0, 7, 3);
    RandomHydrolysis t_1(1, 7, 2);
    RandomHydrolysis t_2(2, 7, 4);
    RandomHydrolysis t_3(3, 7, 9);

    EXPECT_DOUBLE_EQ(21, t_0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_2.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 0, t_3.initial_R(0, filaments, concentrations));
}

TEST(RandomHydrolysis, SingleFilamentPerform) {
    std::vector<State> values;
    values += 0, 1, 0, 0, 2, 1, 0, 1;

    filament_container_t filaments;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values.begin(), values.end())));

    concentration_container_t concentrations;

    RandomHydrolysis t_0(0, 1, 3);
    RandomHydrolysis t_1(1, 2, 2);
    RandomHydrolysis t_2(2, 7, 4);

    // Must call R before perform
    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 4, t_2.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, t_0.perform(0, 2.1, filaments, concentrations));
    EXPECT_DOUBLE_EQ(9, t_0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_1.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(4, t_2.R(0, filaments, concentrations, 0));
    EXPECT_EQ(1, filaments[0]->pointed_state());

    EXPECT_EQ(0, t_0.perform(0, 8, filaments, concentrations));
    EXPECT_DOUBLE_EQ( 6, t_0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(10, t_1.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ( 4, t_2.R(0, filaments, concentrations, 0));
    EXPECT_EQ(1, filaments[0]->barbed_state());

    EXPECT_EQ(0, t_1.perform(0, 9, filaments, concentrations));
    EXPECT_DOUBLE_EQ(6, t_0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_1.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(8, t_2.R(0, filaments, concentrations, 0));
    EXPECT_EQ(2, filaments[0]->barbed_state());
}

TEST(RandomHydrolysis, DoubleFilamentPerform) {
    std::vector<State> values1;
    values1 += 0, 1, 0, 0, 2, 1, 0, 1;
    std::vector<State> values2;
    values2 += 1, 1, 2, 0, 2, 0, 0, 1;

    filament_container_t filaments;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values1.begin(), values1.end())));
    filaments.push_back(filament_ptr_t(new SimpleFilament(values2.begin(), values2.end())));

    concentration_container_t concentrations;

    RandomHydrolysis t_0(0, 1, 3);
    RandomHydrolysis t_1(1, 2, 2);
    RandomHydrolysis t_2(2, 3, 4);

    // Must call R before perform
    EXPECT_DOUBLE_EQ(21, t_0.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_1.initial_R(0, filaments, concentrations));
    EXPECT_DOUBLE_EQ(12, t_2.initial_R(0, filaments, concentrations));

    EXPECT_EQ(1, t_1.perform(0, 7, filaments, concentrations));
    EXPECT_DOUBLE_EQ(21, t_0.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(10, t_1.R(0, filaments, concentrations, 1));
    EXPECT_DOUBLE_EQ(16, t_2.R(0, filaments, concentrations, 1));
    EXPECT_EQ(2, filaments[1]->pointed_state());
}

TEST(RandomHydrolysisWithByproduct, SingleFilamentPerform) {
    std::vector<State> values;
    values += 0, 1, 0, 0, 2, 1, 0, 1;

    filament_container_t filaments;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values.begin(), values.end())));

    concentration_container_t concentrations;
    concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 3)));

    RandomHydrolysisWithByproduct t_0(0, 1, 3, 0);

    EXPECT_DOUBLE_EQ(12, t_0.initial_R(0, filaments, concentrations));

    EXPECT_EQ(0, t_0.perform(0, 1, filaments, concentrations));
    EXPECT_DOUBLE_EQ(9, t_0.R(0, filaments, concentrations, 0));
    EXPECT_DOUBLE_EQ(3, concentrations[0]->value());
}
