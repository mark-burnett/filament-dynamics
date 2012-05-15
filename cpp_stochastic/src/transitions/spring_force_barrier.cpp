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

#include <algorithm>
#include "transitions/spring_force_barrier.h"

#include "barrier_position.h"

namespace stochastic {
namespace transitions {

double RaiseBarrierSpringForce::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    size_t initial_distance = std::max(barrier_position,
            _zero_force_barrier_position)
        - std::min(barrier_position, _zero_force_barrier_position);

    const double initial_energy = std::pow(_barrier_dist_scale * initial_distance, 2);

    size_t final_distance = std::max(barrier_position + 1,
            _zero_force_barrier_position)
        - std::min(barrier_position + 1, _zero_force_barrier_position);

    const double final_energy = std::pow(_barrier_dist_scale * final_distance, 2);

    return _rate_scale * std::exp(-(final_energy - initial_energy) * _energy_scale);
}

double LowerBarrierSpringForce::initial_R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations) {
    // cache filament lengths
    _filament_lengths.reserve(filaments.size());
    _filament_lengths.resize(filaments.size());

    size_t max_length = 0;
    for (size_t fi = 0; fi < _filament_lengths.size(); ++fi) {
        _filament_lengths[fi] = filaments[fi]->length();
        if (max_length < _filament_lengths[fi]) {
            max_length = _filament_lengths[fi];
        }
    }

    if (!_initialized) {
        barrier_position = std::max(_zero_force_barrier_position,
                max_length * _divisions);
        _initialized = true;
    }

    return _check_rate(max_length);
}

double LowerBarrierSpringForce::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    _filament_lengths[previous_filament_index] =
        filaments[previous_filament_index]->length();

    // XXX This is bad, may as well remember the longest filament..
    size_t max_length = 0;
    for (size_t fi = 0; fi < _filament_lengths.size(); ++fi) {
        if (max_length < _filament_lengths[fi]) {
            max_length = _filament_lengths[fi];
        }
    }

    return _check_rate(max_length);
}

double LowerBarrierSpringForce::_check_rate(size_t max_length) {
    if (barrier_position > (max_length * _divisions)) {
        // Note: Our sign convention is that positive force pushes against the filaments.
        size_t initial_distance = std::max(barrier_position,
                _zero_force_barrier_position)
            - std::min(barrier_position, _zero_force_barrier_position);

        const double initial_energy = std::pow(_barrier_dist_scale * initial_distance, 2);

        size_t final_distance = std::max(barrier_position - 1,
                _zero_force_barrier_position)
            - std::min(barrier_position - 1, _zero_force_barrier_position);

        const double final_energy = std::pow(_barrier_dist_scale * final_distance, 2);

        return _rate_scale * std::exp(-(final_energy - initial_energy) * _energy_scale);
    }
    return 0;
}

} // namespace transitions
} // namespace stochastic
