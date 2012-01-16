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

double FixedRateDepolymerization::R(double time,
        const filament_container_t &filaments,
        const concentration_container_t &concentrations) {
    if (_disable_time > 0 && time > _disable_time) {
        _previous_R = 0;
        return 0;
    }

    _previous_R = 0;
    for (filament_container_t::const_iterator fi = filaments.begin();
            fi < filaments.end(); ++fi) {
        if (_state == get_state(**fi)) {
            _previous_R += _rate;
        }
    }

    return _previous_R;
}

size_t FixedRateDepolymerization::perform(double time, double r,
        filament_container_t &filaments,
        concentration_container_t &concentrations) {
    for (filament_container_t::const_iterator fi = filaments.begin();
            fi < filaments.end(); ++fi) {
        if (_state == get_state(**fi)) {
            if (r < _rate) {
                remove_state(**fi);
                concentrations[_state]->add_monomer();
                return ++_count;
            }
            r -= _rate;
        }
    }

    return 0;
}
