#ifndef _SIMULATION_STRATEGY_H_
#define _SIMULATION_STRATEGY_H_
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

#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/variate_generator.hpp>

#include "concentrations/concentration.h"
#include "end_conditions/end_condition.h"
#include "measurements/measurement.h"
#include "filaments/filament.h"
#include "transitions/transition.h"

#include "random_seed.h"

namespace stochastic {

class SimulationStrategy {
    public:
        SimulationStrategy(
                transitions::container_t &transitions,
                concentrations::container_t &concentrations,
                measurements::container_t &measurements,
                end_conditions::container_t &end_conditions,
                filaments::container_t &filaments) :
            _transitions(transitions),
            _concentrations(concentrations),
            _measurements(measurements),
            _end_conditions(end_conditions),
            _filaments(filaments),
            _rng(generate_random_seed()) {}

        measurements::container_t run();

    private:
        transitions::container_t _transitions;
        concentrations::container_t _concentrations;
        measurements::container_t _measurements;
        end_conditions::container_t _end_conditions;
        filaments::container_t _filaments;

        typedef boost::mt19937 _rng_t;
        typedef boost::uniform_real<> _distribution_t;
        typedef boost::variate_generator<_rng_t &, _distribution_t> _variate_t;
        _rng_t _rng;

        std::vector<double> _transition_rates;

        void initialize_simulation();
        double calculate_initial_R(double time);
        double calculate_R(double time, size_t previous_filament_index);
        void record_measurements(double time);
        size_t perform_transition(double time, double r);
        bool end_conditions_not_met(double time);

        double _random(double max);
};

} // namespace stochastic

#endif // _SIMULATION_STRATEGY_H_
