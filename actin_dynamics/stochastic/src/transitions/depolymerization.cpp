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

#include "transitions/depolymerization.h"

namespace stochastic {
namespace transitions {

double FixedRateDepolymerization::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _states.reserve(filaments.size());
    _states.resize(filaments.size());
    if (_disable_time > 0 && time > _disable_time) {
        return 0;
    }

    size_t fi = 0;
    for ( ; fi < filaments.size(); ++fi) {
        State fstate = get_state(*filaments[fi]);
        _states[fi] = fstate;
        if (_state == fstate) {
            ++_count;
        }
    }

    return _rate * _count;
}

double FixedRateDepolymerization::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    if (_disable_time > 0 && time > _disable_time) {
        return 0;
    }
    State previous_state = _states[previous_filament_index];
    State this_state = get_state(*filaments[previous_filament_index]);
    if (_state == previous_state) {
        --_count;
    }
    if (_state == this_state) {
        ++_count;
    }
    return _rate * _count;
}

size_t FixedRateDepolymerization::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    size_t fi = 0;
    for ( ; fi < filaments.size(); ++fi) {
        if (_state == get_state(*filaments[fi])) {
            if (r < _rate) {
                remove_state(*filaments[fi]);
                concentrations[_state]->add_monomer();
                return fi;
            }
            r -= _rate;
        }
    }

    return fi;
}

} // namespace transitions
} // namespace stochastic
