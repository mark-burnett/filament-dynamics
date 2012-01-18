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

#include <boost/assign/std/vector.hpp>

// Bring operator+= into the namespace
using namespace boost::assign;

#include "test_states.h"

#include "simulation_strategy.h"

#include "transitions/random_hydrolysis.h"
#include "concentrations/fixed_concentration.h"
#include "measurements/state_count.h"
#include "filaments/simple_filament.h"
#include "end_conditions/event_count.h"

using namespace stochastic;

TEST(SimulationStrategy, BasicSingleFilamentTest) {
    transitions::container_t transitions;
    concentrations::container_t concentrations;
    measurements::container_t measurements;
    end_conditions::container_t end_conditions;
    filaments::container_t filaments;

    transitions.push_back(transitions::base_ptr_t(
                new transitions::RandomHydrolysis(zero, one, 0.3)));

    end_conditions.push_back(end_conditions::base_ptr_t(
                new end_conditions::EventCount(3)));

    measurements.push_back(measurements::base_ptr_t(
                new measurements::StateCount(zero, 0)));
    measurements.push_back(measurements::base_ptr_t(
                new measurements::StateCount(one, 0)));

    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    filaments.push_back(filaments::base_ptr_t(
                new filaments::SimpleFilament(values)));

    SimulationStrategy ss(transitions, concentrations, measurements,
            end_conditions, filaments);

    measurements::container_t results(ss.run());

    // 5 measurements means 4 events.
    EXPECT_EQ(5, results[0]->get_values()[0].size());
    EXPECT_EQ(5, results[1]->get_values()[0].size());

    EXPECT_EQ(4, results[0]->get_values()[0][0]);
    EXPECT_EQ(3, results[1]->get_values()[0][0]);

    EXPECT_EQ(3, results[0]->get_values()[0][2]);
    EXPECT_EQ(4, results[1]->get_values()[0][2]);

    // Last even occurred, but wasn't measured
    EXPECT_EQ(1, results[0]->get_values()[0].back());
    EXPECT_EQ(6, results[1]->get_values()[0].back());
}
