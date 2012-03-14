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

#include "transitions/barrier.h"

#include "barrier_position.h"

namespace stochastic {
namespace transitions {

double LowerBarrier::initial_R(double time,
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

    if (!_barrier_initialized) {
        barrier_position = max_length * _divisions + 1;
        _barrier_initialized = true;
    }

    return _check_rate(max_length);
}

double LowerBarrier::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    _filament_lengths[previous_filament_index] =
        filaments[previous_filament_index]->length();

    size_t max_length = 0;
    for (size_t fi = 0; fi < _filament_lengths.size(); ++fi) {
        if (max_length < _filament_lengths[fi]) {
            max_length = _filament_lengths[fi];
        }
    }

    return _check_rate(max_length);
}

double LowerBarrier::_check_rate(size_t max_length) {
    if (barrier_position > (max_length * _divisions)) {
        return _rate;
    }
    return 0;
}


double BarrierBarbedEndPolymerization::initial_R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations) {
    size_t count = 0;
    size_t position_in_subunits = barrier_position / _divisions;
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        if (position_in_subunits > filaments[fi]->length()) {
            ++count;
        }
    }
    return count * _rate;
}

double BarrierBarbedEndPolymerization::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    return initial_R(time, filaments, concentrations);
}

size_t BarrierBarbedEndPolymerization::perform(double time, double r,
            filaments::container_t &filaments,
            concentrations::container_t &concentrations) {
    size_t count = r / _rate;
    size_t position_in_subunits = barrier_position / _divisions;
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        if (position_in_subunits > filaments[fi]->length()) {
            if (0 == count) {
                filaments[fi]->append_barbed(_state);
                return fi;
            }
            --count;
        }
    }
    return 0;
}

} // namespace transitions
} // namespace stochastic
