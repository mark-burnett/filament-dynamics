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

#include "transitions/random_hydrolysis.h"

namespace stochastic {
namespace transitions {

double RandomHydrolysis::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _filament_counts.reserve(filaments.size());
    _filament_counts.resize(filaments.size());

    size_t fc;
    for (size_t i = 0; i < filaments.size(); ++i) {
        fc = filaments[i]->state_count(_old_state);
        _filament_counts[i] = fc;
        _count += fc;
    }

    return _rate * _count;
}

double RandomHydrolysis::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    size_t previous_count = _filament_counts[previous_filament_index];
    size_t this_count = filaments[previous_filament_index]->state_count(_old_state);

    _filament_counts[previous_filament_index] = this_count;

    _count += this_count;
    _count -= previous_count;

    return _rate * _count;
}

size_t RandomHydrolysis::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    size_t total_number = r / _rate;
    size_t i = 0;
    while (total_number >= _filament_counts[i]) {
        total_number -= _filament_counts[i];
        ++i;
    }
    filaments[i]->update_state(total_number, _old_state, _new_state);
    return i;
}

} // namespace transitions
} // namespace stochastic
