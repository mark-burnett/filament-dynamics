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

#include <cmath>
#include <algorithm>

#include "simulation_strategy.h"
#include "barrier_position.h"

namespace stochastic {

measurements::container_t SimulationStrategy::run() {
    size_t transition_count = 0;
    double time = 0;

    initialize_simulation();

    size_t previous_filament_index = 0;

    // Calculate rates for the next timestep.
    double R = calculate_initial_R(time);
    // First update the time & perform measurements
    time += _get_time_delta(R);

    record_measurements(time);

    // Decide which transition to perform.
    double r = _random(R);

    previous_filament_index = perform_transition(time, r);
    ++transition_count;

    while (end_conditions_not_met(time)) {
        // Calculate rates for the next timestep.
        R = calculate_R(time, previous_filament_index);
        if (0 == R) {
            // We should never really get here.
            // If we do, try to recover by re-initializing rates.
            R = calculate_initial_R(time);
            if (0 == R) {
//                break;
                throw std::exception();
            }
        }

        // First update the time & perform measurements
        time += _get_time_delta(R);
        record_measurements(time);

        // Decide which transition to perform.
        r = _random(R);

        previous_filament_index = perform_transition(time, r);
        ++transition_count;
    }

    return _measurements;
}


void SimulationStrategy::initialize_simulation() {
    _transition_rates.reserve(_transitions.size());
    _transition_rates.resize(_transitions.size());

    for (measurements::container_t::iterator mi = _measurements.begin();
            mi != _measurements.end(); ++mi) {
        mi->second->initialize(_filaments, _concentrations);
    }
    // Initialize end conditions
    for (end_conditions::container_t::iterator ei = _end_conditions.begin();
            ei < _end_conditions.end(); ++ei) {
        (*ei)->initialize(_filaments, _concentrations);
    }
}

double SimulationStrategy::calculate_initial_R(double time) {
    double R = 0;
    for (size_t ti = 0; ti < _transitions.size(); ++ti) {
        _transition_rates[ti] = _transitions[ti]->initial_R(time,
                _filaments, _concentrations);
        R += _transition_rates[ti];
    }
    return R;
}

double SimulationStrategy::calculate_R(double time,
        size_t previous_filament_index) {
    double R = 0;
    for (size_t ti = 0; ti < _transitions.size(); ++ti) {
        _transition_rates[ti] = _transitions[ti]->R(time,
                _filaments, _concentrations, previous_filament_index);
        R += _transition_rates[ti];
    }
    return R;
}

void SimulationStrategy::record_measurements(double time) {
    for (measurements::container_t::iterator mi = _measurements.begin();
            mi != _measurements.end(); ++mi) {
        mi->second->perform(time, _filaments, _concentrations);
    }
}

size_t SimulationStrategy::perform_transition(double time, double r) {
    for (size_t ti = 0; ti < _transition_rates.size(); ++ti) {
        // Just avoiding rounding errors.
        r = std::max(0.0, r);
        if (r < _transition_rates[ti]) {
            return _transitions[ti]->perform(time, r, _filaments, _concentrations);
        }
        r -= _transition_rates[ti];
    }
    return 0;
}

bool SimulationStrategy::end_conditions_not_met(double time) {
    for (end_conditions::container_t::iterator eci = _end_conditions.begin();
            eci < _end_conditions.end(); ++eci) {
        if ((*eci)->satisfied(time, _filaments, _concentrations)) {
            return false;
        }
    }
    return true;
}

double SimulationStrategy::_get_time_delta(double R) {
    double r = 0;
    while (0 == r) {
        r = _random(1);
    }
    return log(1 / r) / R;
}

double SimulationStrategy::_random(double max) {
    _distribution_t d(0, max);
    _variate_t vg(_rng, d);
    return vg();
}

}
