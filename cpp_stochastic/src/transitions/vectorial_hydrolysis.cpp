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

#include "transitions/vectorial_hydrolysis.h"

namespace stochastic {
namespace transitions {

double VectorialHydrolysis::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _filament_counts.reserve(filaments.size());
    _filament_counts.resize(filaments.size());

    size_t fc;
    _count = 0;
    for (size_t i = 0; i < filaments.size(); ++i) {
        fc = filaments[i]->boundary_count(_pointed_neighbor, _old_state);
        _filament_counts[i] = fc;
        _count += fc;
    }

    return _rate * _count;
}

double VectorialHydrolysis::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    size_t previous_count = _filament_counts[previous_filament_index];
    size_t this_count = filaments[previous_filament_index]->boundary_count(
            _pointed_neighbor, _old_state);

    _filament_counts[previous_filament_index] = this_count;

    _count += this_count;
    _count -= previous_count;

    return _rate * _count;
}

size_t VectorialHydrolysis::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    size_t total_number = r / _rate;
    for (size_t i = 0; i < _filament_counts.size(); ++i) {
        if (total_number < _filament_counts[i]) {
            filaments[i]->update_boundary(total_number,
                    _pointed_neighbor, _old_state, _new_state);
            return i;
        }
        total_number -= _filament_counts[i];
    }
    return 0;
}

} // namespace transitions
} // namespace stochastic
