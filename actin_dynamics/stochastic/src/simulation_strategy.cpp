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

#include "simulation_strategy.h"

void SimulationStrategy::run() {
    double time = 0;

    initialize_simulation();

    std::vector<double> transition_rates;
    transition_rates.resize(_transitions.size());

    while (end_conditions_not_met(time)) {
        // Calculate rates for the next timestep.
        double R = 0;
        for (size_t ti = 0; ti < _transitions.size(); ++ti) {
            transition_rates[ti] = _transitions[ti]->R(time,
                    _filaments, _concentrations);
            R += transition_rates[ti];
        }

        // First update the time & perform measurements
        time += log(1 / _random(1)) / R;
        record_measurements(time);

        // Decide which transition to perform.
        double r = _random(R);
        for (size_t ti = 0; ti < _transitions.size(); ++ti) {
            if (r < transition_rates[ti]) {
                _transitions[ti]->perform(time, r, _filaments, _concentrations);
                break;
            }
            r -= transition_rates[ti];
        }
    }

    // report results
}


void SimulationStrategy::initialize_simulation() {
    for (measurement_container_t::iterator mi = _measurements.begin();
            mi < _measurements.end(); ++mi) {
        (*mi)->initialize(_filaments, _concentrations);
    }
    // Initialize end conditions
    for (end_condition_container_t::iterator ei = _end_conditions.begin();
            ei < _end_conditions.end(); ++ei) {
        (*ei)->initialize(_filaments, _concentrations);
    }
}

void SimulationStrategy::record_measurements(double time) {
    for (measurement_container_t::iterator mi = _measurements.begin();
            mi < _measurements.end(); ++mi) {
        (*mi)->perform(time, _filaments, _concentrations);
    }
}

bool SimulationStrategy::end_conditions_not_met(double time) {
    for (end_condition_container_t::iterator eci = _end_conditions.begin();
            eci < _end_conditions.end(); ++eci) {
        if ((*eci)->satisfied(time, _filaments, _concentrations)) {
            return false;
        }
    }
    return true;
}
