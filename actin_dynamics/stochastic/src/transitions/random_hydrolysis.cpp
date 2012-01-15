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

double RandomHydrolysis::R(double time, const filament_container_t &filaments,
        const concentration_container_t &concentrations) {
    filament_Rs.resize(filaments.size());

    double r;
    previous_R = 0;
    for (size_t i = 0; i < filaments.size(); ++i) {
        r = rate * filaments[i]->state_count(old_state);
        filament_Rs[i] = r;
        previous_R += r;
    }

    return previous_R;
}

size_t RandomHydrolysis::perform(double time, double r,
        filament_container_t &filaments,
        concentration_container_t &concentrations) {
    for (size_t i = 0; i < filaments.size(); ++i) {
        double filament_R = filament_Rs[i];
        if (r < filament_R) {
            size_t number = r / rate;
            filaments[i]->update_state(number, old_state, new_state);
            return ++count;
        }
        r -= filament_R;
    }
    return 0;
}
