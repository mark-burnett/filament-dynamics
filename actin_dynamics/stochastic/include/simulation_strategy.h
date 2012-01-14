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

class SimulationStrategy {
    public:
        SimulationStrategy() : _rng(generate_random_seed()) {}

        SimulationStrategy(transition_container_t &transitions,
                concentration_container_t &concentrations,
                measurement_container_t &measurements,
                end_condition_container_t &end_conditions,
                filament_container_t &filaments) :
            _transitions(transitions),
            _concentrations(concentrations),
            _measurements(measurements),
            _end_conditions(end_conditions),
            _filaments(filaments),
            _rng(generate_random_seed()) {}

        // XXX Fix return value (concentration and filament measurements)
        void run();

        inline double _random(double max) {
            _distribution_t d(0, max);
            _variate_t vg(_rng, d);
            return vg();
        };

    private:
        transition_container_t _transitions;
        concentration_container_t _concentrations;
        measurement_container_t _measurements;
        end_condition_container_t _end_conditions;
        filament_container_t _filaments;

        typedef boost::mt19937 _rng_t;
        typedef boost::uniform_real<> _distribution_t;
        typedef boost::variate_generator<_rng_t, _distribution_t> _variate_t;
        _rng_t _rng;
};

#endif // _SIMULATION_STRATEGY_H_
