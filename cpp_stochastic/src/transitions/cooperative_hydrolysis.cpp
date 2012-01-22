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

#include "transitions/cooperative_hydrolysis.h"

namespace stochastic {
namespace transitions {

double CooperativeHydrolysis::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _random_R = _random_transition.initial_R(time, filaments, concentrations);
    _vectorial_R = _vectorial_transition.initial_R(time, filaments,
            concentrations);
    return _random_R + _vectorial_R;
}

double CooperativeHydrolysis::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    _random_R = _random_transition.R(time, filaments, concentrations,
            previous_filament_index);
    _vectorial_R = _vectorial_transition.R(time, filaments, concentrations,
            previous_filament_index);
    return _random_R + _vectorial_R;
}

size_t CooperativeHydrolysis::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    if (r < _random_R) {
        return _random_transition.perform(time, r, filaments, concentrations);
    }
    return _vectorial_transition.perform(time, r - _random_R,
            filaments, concentrations);
}

} // namespace transitions
} // namespace stochastic
