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

#include "transitions/barrier_polymerization.h"

#include "barrier_position.h"

namespace stochastic {
namespace transitions {

double StepFunctionBarrierBarbedEndPolymerization::initial_R(double time,
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

double StepFunctionBarrierBarbedEndPolymerization::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    return initial_R(time, filaments, concentrations);
}

size_t StepFunctionBarrierBarbedEndPolymerization::perform(double time, double r,
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

double LinearFunctionBarrierBarbedEndPolymerization::initial_R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations) {
    double R = 0;
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        _filament_rates[fi] = _filament_rate(filaments[fi]->length());
        R += _filament_rates[fi];
    }
    return R;
}

double LinearFunctionBarrierBarbedEndPolymerization::_filament_rate(
        size_t length) {
    size_t d = barrier_position - (length * _divisions);
    if (d >= _linear_width) {
        return _rate;
    } else if (d < _divisions) {
        return 0;
    } else {
        return d * _slope;
    }
}

double LinearFunctionBarrierBarbedEndPolymerization::R(double time,
            const filaments::container_t &filaments,
            const concentrations::container_t &concentrations,
            size_t previous_filament_index) {
    _filament_rates.reserve(filaments.size());
    _filament_rates.resize(filaments.size());
    return initial_R(time, filaments, concentrations);
}

size_t LinearFunctionBarrierBarbedEndPolymerization::perform(
            double time, double r,
            filaments::container_t &filaments,
            concentrations::container_t &concentrations) {
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        r = std::max(0.0, r);
        if (r < _filament_rates[fi]) {
            filaments[fi]->append_barbed(_state);
            return fi;
        }
        r -= _filament_rates[fi];
    }
    throw std::exception();
}

} // namespace transitions
} // namespace stochastic
