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

#include "concentrations/concentration.h"
#include "end_conditions/end_condition.h"
#include "filaments/filament.h"
#include "measurements/measurement.h"
#include "transitions/transition.h"

#include "concentrations/fixed_reagent.h"

#include "end_conditions/duration.h"

#include "filaments/default_filament.h"

#include "measurements/concentration.h"
#include "measurements/filament_length.h"

#include "transitions/association.h"
#include "transitions/cooperative_hydrolysis.h"
#include "transitions/depolymerization.h"
#include "transitions/monomer.h"
#include "transitions/polymerization.h"
#include "transitions/random_hydrolysis.h"
#include "transitions/tip_hydrolysis.h"

using namespace stochastic;

const size_t number_of_filaments = 10;

const double fnc = 0.00179;
const double seed_concentration = 6;

const double initial_concentration = 30;

const double duration = 2500.1;
const double sample_period = 1;

const double hydrolysis_rate = 0.3;
const double dissociation_cooperativity = 1e11;
const double dissociation_rate = 1.47e-7;

const double b_atp_assoc_rate = 11.6;
const double b_adppi_assoc_rate = 3.4;
const double b_adp_assoc_rate = 2.9;

const double b_atp_dissoc_rate = 1.4;
const double b_adppi_dissoc_rate = 0.2;
const double b_adp_dissoc_rate = 5.4;

const double p_atp_assoc_rate = 1.3;
const double p_adppi_assoc_rate = 0.11;
const double p_adp_assoc_rate = 0.14;

const double p_atp_dissoc_rate = 0.8;
const double p_adppi_dissoc_rate = 0.02;
const double p_adp_dissoc_rate = 0.25;

const double b_tip_pi_dissoc_rate = 2;

const double sol_pi_dissoc_rate = 10000;

const double pi_association_rate = 2e-6;

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
                new concentrations::FixedReagent(initial_concentration,
                    fnc, number_of_filaments));

    concentrations[adppi] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(0,
                    fnc, number_of_filaments));

    concentrations[adp] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(0,
                    fnc, number_of_filaments));

    concentrations[pi] = concentrations::Concentration::ptr_t(
                new concentrations::FixedReagent(0,
                    fnc, number_of_filaments));


    // --- end conditions
    end_conditions.push_back(end_conditions::EndCondition::ptr_t(
                new end_conditions::Duration(duration)));


    // --- filaments
    for (size_t i = 0; i < number_of_filaments; ++i) {
        filaments.push_back(filaments::Filament::ptr_t(
                new filaments::DefaultFilament(seed_concentration, fnc, adp)));
    }


    // --- measurements
    measurements["length"] = measurements::Measurement::ptr_t(
            new measurements::FilamentLength(sample_period));
    measurements["Pi"] = measurements::Measurement::ptr_t(
            new measurements::Concentration(pi, sample_period));


    // --- interesting transitions
    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::Association(pi, adp, adppi,
                    pi_association_rate)));


    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::RandomHydrolysis(atp, adppi,
                    hydrolysis_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::CooperativeHydrolysisWithByproduct(adp, adppi,
                    adp, dissociation_rate, pi, dissociation_cooperativity)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedTipHydrolysisWithByproduct(adppi, adp,
                    b_tip_pi_dissoc_rate, pi)));


    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::Monomer(adppi, adp,
                    sol_pi_dissoc_rate)));



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
                new transitions::PointedEndDepolymerization(
                    atp, p_atp_dissoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::PointedEndDepolymerization(
                    adppi, p_adppi_dissoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::PointedEndDepolymerization(
                    adp, p_adp_dissoc_rate)));


    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndPolymerization(
                    atp, b_atp_assoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndPolymerization(
                    adppi, b_adppi_assoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::BarbedEndPolymerization(
                    adp, b_adp_assoc_rate)));


    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::PointedEndPolymerization(
                    atp, p_atp_assoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::PointedEndPolymerization(
                    adppi, p_adppi_assoc_rate)));

    transitions.push_back(transitions::Transition::ptr_t(
                new transitions::PointedEndPolymerization(
                    adp, p_adp_assoc_rate)));


    // --- construct and run simulation
    SimulationStrategy sim(transitions, concentrations, measurements,
            end_conditions, filaments);

    sim.run();

    return 0;
}
