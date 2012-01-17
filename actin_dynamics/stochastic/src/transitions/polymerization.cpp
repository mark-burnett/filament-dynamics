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

#include "transitions/polymerization.h"

#include <iostream>
double FixedRatePolymerization::initial_R(double time,
        const filament_container_t &filaments,
        const concentration_container_t &concentrations) {
    if (_disable_time > 0 && time > _disable_time) {
        return 0;
    }

    return _rate * concentrations[_state]->value() * filaments.size();
}

double FixedRatePolymerization::R(double time,
        const filament_container_t &filaments,
        const concentration_container_t &concentrations,
        size_t previous_filament_index) {
    return initial_R(time, filaments, concentrations);
}

size_t FixedRatePolymerization::perform(double time, double r,
        filament_container_t &filaments,
        concentration_container_t &concentrations) {
    double filament_r = _rate * concentrations[_state]->value();
    size_t number = r / filament_r;
    append_state(*filaments[number]);
    concentrations[_state]->remove_monomer();
    return number;
}
