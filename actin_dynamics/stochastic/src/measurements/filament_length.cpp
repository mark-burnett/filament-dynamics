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

#include "measurements/filament_length.h"

void FilamentLength::initialize(const filament_container_t &filaments,
                const concentration_container_t &concentrations) {
    _lengths.reserve(filaments.size());
    _lengths.resize(filaments.size());

    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        // XXX I could reserve and resize these right now if i knew the duration and sample time
        _lengths[fi].push_back(filaments[fi]->length());
    }

    _times.push_back(0);
}

void FilamentLength::perform(double time,
        const filament_container_t &filaments,
        const concentration_container_t &concentrations) {
    if (time - _times.back() > _sample_period) {
        // XXX do measurement
    }
}
