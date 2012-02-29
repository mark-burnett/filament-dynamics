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

#include "transitions/tip_hydrolysis.h"

namespace stochastic {
namespace transitions {

double TipHydrolysis::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _states.reserve(filaments.size());
    _states.resize(filaments.size());
    size_t fi = 0;
    _count = 0;
    for ( ; fi < filaments.size(); ++fi) {
        State fstate = get_state(*filaments[fi]);
        _states[fi] = fstate;
        if (_old_state == fstate) {
            ++_count;
        }
    }

    return _rate * _count;
}

double TipHydrolysis::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    State previous_state = _states[previous_filament_index];
    State this_state = get_state(*filaments[previous_filament_index]);
    _states[previous_filament_index] = this_state;

    if (_old_state == previous_state) {
        --_count;
    }
    if (_old_state == this_state) {
        ++_count;
    }

    return _rate * _count;
}

size_t TipHydrolysis::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        if (_old_state == get_state(*filaments[fi])) {
            if (r < _rate) {
                perform_filament(*filaments[fi]);
                return fi;
            }
            r -= _rate;
            r = std::max(r, 0.0);
        }
    }

    return 0;
}

} // namespace transitions
} // namespace stochastic
