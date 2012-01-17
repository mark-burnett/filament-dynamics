//    Copyright (C) 2012 Mark Burnett
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by //    the Free Software Foundation, either version 3 of the License, or
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
#include "transitions/polymerization.h"
#include "concentrations/fixed_reagent.h"
#include "measurements/state_count.h"
#include "measurements/filament_length.h"
#include "filaments/cached_filament.h"
#include "end_conditions/duration.h"

TEST(Integration, OldBasicTest) {
    const size_t number_of_filaments = 1000;

    transition_container_t transitions;
    concentration_container_t concentrations;
    measurement_container_t measurements;
    end_condition_container_t end_conditions;
    filament_container_t filaments;

    transitions.push_back(
            transition_ptr_t(new RandomHydrolysisWithByproduct(0, 1, 0.3, 2)));
    transitions.push_back(transition_ptr_t(new BarbedEndPolymerization(0, 10)));

    end_conditions.push_back(end_condition_ptr_t(new Duration(40)));

    measurements.push_back(measurement_ptr_t(new StateCount(0, 0.1)));
    measurements.push_back(measurement_ptr_t(new StateCount(1, 0.1)));
    measurements.push_back(measurement_ptr_t(new StateCount(2, 0.1)));
    measurements.push_back(measurement_ptr_t(new FilamentLength(0.1)));

    for (size_t i = 0; i < number_of_filaments; ++i) {
        filaments.push_back(filament_ptr_t(new CachedFilament(6/0.0112, 1)));
    }

    concentrations.push_back(concentration_ptr_t(new FixedReagent(6, 0.0112,
                    number_of_filaments)));
    concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 0.0112,
                    number_of_filaments)));
    concentrations.push_back(concentration_ptr_t(new FixedReagent(0, 0.0112,
                    number_of_filaments)));

    SimulationStrategy ss(transitions, concentrations, measurements,
            end_conditions, filaments);

    measurement_container_t results(ss.run());
}
