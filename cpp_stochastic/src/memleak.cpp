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

#include "state.h"
#include "simulation_strategy.h"

#include "barrier_position.h"

#include "concentrations/concentration.h"
#include "end_conditions/end_condition.h"
#include "filaments/filament.h"
#include "measurements/measurement.h"
#include "transitions/transition.h"

#include "concentrations/fixed_concentration.h"

#include "end_conditions/duration.h"

#include "filaments/default_filament.h"

#include "measurements/concentration.h"
#include "measurements/filament_length.h"

#include "transitions/cooperative_hydrolysis.h"
#include "transitions/depolymerization.h"
#include "transitions/barrier_polymerization.h"
#include "transitions/spring_force_barrier.h"
#include "transitions/random_hydrolysis.h"

using namespace stochastic;

const size_t number_of_filaments = 1;

const double fnc = 0.002;
const double seed_concentration = 20;

const double initial_concentration = 0.3;

const double duration = 1000;
const double sample_period = 1;

const double hydrolysis_rate = 0.3;
const double dissociation_rate = 0.00162833767016;

const double b_atp_assoc_rate = 11.6;
const double b_adppi_assoc_rate = 3.4;
const double b_adp_assoc_rate = 2.9;

const double b_atp_dissoc_rate = 1.4;
const double b_adppi_dissoc_rate = 0.2;
const double b_adp_dissoc_rate = 5.4;

// These values match the python version
const size_t divisions = 10;
const size_t rest_position = 100100;
const double spring_constant = 8.0e-6;
const double D = 1.0e-14;

int main(int argc, char *argv[]) {
    const State atp("ATP");
    const State adppi("ADPPi");
    const State adp("ADP");
    const State pi("Pi");

    concentrations::container_t concentrations;
    end_conditions::container_t end_conditions;
    filaments::container_t filaments;
    measurements::container_t measurements;
    transitions::container_t transitions;


    // --- concentrations
    concentrations[atp] = concentrations::Concentration::ptr_t(
                new concentrations::FixedConcentration(
                    initial_concentration));

    concentrations[adppi] = concentrations::Concentration::ptr_t(
                new concentrations::FixedConcentration(0));

    concentrations[adp] = concentrations::Concentration::ptr_t(
                new concentrations::FixedConcentration(0));

    concentrations[pi] = concentrations::Concentration::ptr_t(
                new concentrations::FixedConcentration(0));


    // --- end conditions
    end_conditions.push_back(end_conditions::EndCondition::ptr_t(
                new end_conditions::Duration(duration)));


    // --- filaments
    for (size_t i = 0; i < number_of_filaments; ++i) {
        filaments.push_back(filaments::Filament::ptr_t(
                new filaments::DefaultFilament(seed_concentration, fnc, adp)));
    }


    // --- measurements
//    measurements["length"] = measurements::Measurement::ptr_t(
//            new measurements::FilamentLength(sample_period));


    // --- hydrolysis transitions
    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::RandomHydrolysis(atp, adppi,
                    hydrolysis_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::RandomHydrolysisWithByproduct(adppi, adp,
                    dissociation_rate, pi)));

    // --- poly/depoly transitions
    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndDepolymerization(
                    atp, b_atp_dissoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndDepolymerization(
                    adppi, b_adppi_dissoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndDepolymerization(
                    adp, b_adp_dissoc_rate)));


    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::StepFunctionBarrierBarbedEndPolymerization(
                    atp, b_atp_assoc_rate, divisions)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::StepFunctionBarrierBarbedEndPolymerization(
                    adppi, b_adppi_assoc_rate, divisions)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::StepFunctionBarrierBarbedEndPolymerization(
                    adp, b_adp_assoc_rate, divisions)));

    // barrier movement transitions
    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::RaiseBarrierSpringForce(
                    spring_constant, rest_position, D, divisions)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::LowerBarrierSpringForce(
                    spring_constant, rest_position, D, divisions)));


    // --- construct and run simulation
    SimulationStrategy sim(transitions, concentrations, measurements,
            end_conditions, filaments);

    std::cout << "Initial barrier position " << barrier_position << std::endl;
    std::cout << "Initial filament length " << filaments[0]->length() << std::endl;

    sim.run();

    std::cout << "Final barrier position " << barrier_position << std::endl;
    std::cout << "Final filament length " << filaments[0]->length() << std::endl;

    return 0;
}
