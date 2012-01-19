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

#include <vector>
#include <string>

#include <boost/python.hpp>
// #include <boost/python/implicit.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "state.h"
#include "simulation_strategy.h"

#include "concentrations/concentration.h"
#include "end_conditions/end_condition.h"
#include "filaments/filament.h"
#include "measurements/measurement.h"
#include "transitions/transition.h"

using namespace boost::python;
using namespace stochastic;

void concentrations_level_definitions();
void end_conditions_level_definitions();
void filaments_level_definitions();
void measurements_level_definitions();
void transitions_level_definitions();

void package_level_definitions() {
    // import state
    class_<State>("State", init<const std::string &>());

    // create some vector types
    class_< concentrations::container_t >("ConcentrationContainer")
        .def(map_indexing_suite< concentrations::container_t >());
    class_< end_conditions::container_t >("EndConditionContainer")
        .def(vector_indexing_suite< end_conditions::container_t >());
    class_< filaments::container_t >("FilamentContainer")
        .def(vector_indexing_suite< filaments::container_t >());
    class_< measurements::container_t >("MeasurementContainer")
        .def(vector_indexing_suite< measurements::container_t >());
    class_< transitions::container_t >("TransitionContainer")
        .def(vector_indexing_suite< transitions::container_t >());

    // add conversions for string <-> flyweight
//    implicitly_convertible<std::string, State>();
//    implicitly_convertible<State, std::string>();

    class_<SimulationStrategy>("SimulationStrategy", init<
            transitions::container_t &, concentrations::container_t &,
            measurements::container_t &, end_conditions::container_t &,
            filaments::container_t &>())
        .def("run", &SimulationStrategy::run);
}

BOOST_PYTHON_MODULE(stochasticpy) {
    // Set this up as a package
    object package = scope();
    package.attr("__path__") = "stochasticpy";

    package_level_definitions();

    // Modules
    object concentrations_module(borrowed(
                PyImport_AddModule("stochasticpy.concentrations")));
    package.attr("concentrations") = concentrations_module;

    object end_conditions_module(borrowed(
                PyImport_AddModule("stochasticpy.end_conditions")));
    package.attr("end_conditions") = end_conditions_module;

    object filaments_module(borrowed(
                PyImport_AddModule("stochasticpy.filaments")));
    package.attr("filaments") = filaments_module;

    object measurements_module(borrowed(
                PyImport_AddModule("stochasticpy.measurements")));
    package.attr("measurements") = measurements_module;

    object transitions_module(borrowed(
                PyImport_AddModule("stochasticpy.transitions")));
    package.attr("transitions") = transitions_module;


    // Load concentrations module
    {
        scope concentration_scope = concentrations_module;
        concentrations_level_definitions();
    }

    // Load end_conditions module
    {
        scope end_condition_scope = end_conditions_module;
        end_conditions_level_definitions();
    }

    // Load filaments module
    {
        scope filament_scope = filaments_module;
        filaments_level_definitions();
    }

    // Load measurements module
    {
        scope measurement_scope = measurements_module;
        measurements_level_definitions();
    }

    // Load transitions module
    {
        scope transition_scope = transitions_module;
        transitions_level_definitions();
    }
}
