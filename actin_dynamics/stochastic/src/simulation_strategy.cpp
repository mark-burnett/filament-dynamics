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

namespace stochastic {

measurements::container_t SimulationStrategy::run() {
    double time = 0;

    initialize_simulation();

    std::vector<double> transition_rates;
    transition_rates.resize(_transitions.size());

    size_t previous_filament_index = 0;

    // Calculate rates for the next timestep.
    double R = 0;
    for (size_t ti = 0; ti < _transitions.size(); ++ti) {
        transition_rates[ti] = _transitions[ti]->initial_R(time,
                _filaments, _concentrations);
        R += transition_rates[ti];
    }

    // First update the time & perform measurements
    time += log(1 / _random(1)) / R;

    record_measurements(time);

    // Decide which transition to perform.
    double r = _random(R);

    for (size_t ti = 0; ti < transition_rates.size(); ++ti) {
        if (r < transition_rates[ti]) {
//            std::cout << "ti = " << ti << " of " << _transitions.size()
//                << std::endl;
            previous_filament_index = _transitions[ti]->perform(time, r,
                    _filaments, _concentrations);
            break;
        }
        r -= transition_rates[ti];
    }

    while (end_conditions_not_met(time)) {
        // Calculate rates for the next timestep.
        R = 0;
        for (size_t tip = 0; tip < _transitions.size(); ++tip) {
            transition_rates[tip] = _transitions[tip]->R(time,
                    _filaments, _concentrations, previous_filament_index);
            R += transition_rates[tip];
//            std::cout << tip << " -> " << transition_rates[tip] << std::endl;
        }
        if (0 == R) {
            break;
        }

        // First update the time & perform measurements
        time += log(1 / _random(1)) / R;
        record_measurements(time);

        // Decide which transition to perform.
        r = _random(R);

//        std::cout << "r = " << r << " of " << R << std::endl;

        for (size_t ti = 0; ti < transition_rates.size(); ++ti) {
            if (r < transition_rates[ti]) {
//                std::cout << "ti = " << ti << " of " << _transitions.size()
//                    << std::endl;
                previous_filament_index = _transitions[ti]->perform(time, r,
                        _filaments, _concentrations);
                break;
            }
            r -= transition_rates[ti];
        }

//        std::cout << "lap, pfi = " << previous_filament_index << std::endl;
    }

    return _measurements;
}


void SimulationStrategy::initialize_simulation() {
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

void SimulationStrategy::record_measurements(double time) {
    for (measurements::container_t::iterator mi = _measurements.begin();
            mi != _measurements.end(); ++mi) {
        mi->second->perform(time, _filaments, _concentrations);
    }
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

}
