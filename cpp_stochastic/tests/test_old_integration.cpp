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

#include "test_states.h"

#include "simulation_strategy.h"

#include "transitions/random_hydrolysis.h"
#include "transitions/polymerization.h"
#include "concentrations/fixed_reagent.h"
#include "measurements/state_count.h"
#include "measurements/filament_length.h"
#include "filaments/default_filament.h"
#include "end_conditions/duration.h"

using namespace stochastic;

TEST(Integration, OldBasicTest) {
    const size_t number_of_filaments = 5;

    transitions::container_t transitions;
    concentrations::container_t concentrations;
    measurements::container_t measurements;
    end_conditions::container_t end_conditions;
    filaments::container_t filaments;

    transitions.push_back(
            transitions::end_condition::ptr_t(
                new transitions::RandomHydrolysisWithByproduct(zero, one,
                    0.3, two)));
    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndPolymerization(zero, 10)));

    end_conditions.push_back(end_conditions::EndCondition::ptr_t(
                new end_conditions::Duration(40)));

    measurements["a"] = measurements::Measurement::ptr_t(
                new measurements::StateCount(zero, 0.1));
    measurements["b"] = measurements::Measurement::ptr_t(
                new measurements::StateCount(one, 0.1));
    measurements["c"] = measurements::Measurement::ptr_t(
                new measurements::StateCount(two, 0.1));
    measurements["d"] = measurements::Measurement::ptr_t(
                new measurements::FilamentLength(0.1));

    for (size_t i = 0; i < number_of_filaments; ++i) {
        filaments.push_back(filaments::Filament::ptr_t(
                    new filaments::DefaultFilament(6/0.0112, one)));
    }

    concentrations[zero] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(6, 0.0112,
                    number_of_filaments));
    concentrations[one] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(0, 0.0112,
                    number_of_filaments));
    concentrations[two] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(0, 0.0112,
                    number_of_filaments));

    SimulationStrategy ss(transitions, concentrations, measurements,
            end_conditions, filaments);

    measurements::container_t results(ss.run());
}
