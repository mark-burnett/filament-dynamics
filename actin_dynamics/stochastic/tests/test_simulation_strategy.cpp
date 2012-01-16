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

#include "simulation_strategy.h"

#include "transitions/random_hydrolysis.h"
#include "concentrations/fixed_concentration.h"
#include "measurements/state_count.h"
#include "filaments/simple_filament.h"
#include "end_conditions/event_count.h"

TEST(SimulationStrategy, BasicSingleFilamentTest) {
    transition_container_t transitions;
    concentration_container_t concentrations;
    measurement_container_t measurements;
    end_condition_container_t end_conditions;
    filament_container_t filaments;

    transitions.push_back(transition_ptr_t(new RandomHydrolysis(0, 1, 0.3)));

    end_conditions.push_back(end_condition_ptr_t(new EventCount(4)));

    measurements.push_back(measurement_ptr_t(new StateCount(0, 0)));
    measurements.push_back(measurement_ptr_t(new StateCount(1, 0)));

    std::vector<State> values;
    values += 0, 1, 0, 0, 2, 1, 0, 1;
    filaments.push_back(filament_ptr_t(new SimpleFilament(values)));

    SimulationStrategy ss(transitions, concentrations, measurements,
            end_conditions, filaments);

    measurement_container_t results(ss.run());

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
