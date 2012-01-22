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

#include "transitions/monomer.h"

namespace stochastic {
namespace transitions {

double Monomer::initial_R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    return _rate * concentrations.find(_old_state)->second->monomer_count();
}

double Monomer::R(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations,
        size_t previous_filament_index) {
    return initial_R(time, filaments, concentrations);
}

size_t Monomer::perform(double time, double r,
        filaments::container_t &filaments,
        concentrations::container_t &concentrations) {
    concentrations[_old_state]->remove_monomer();
    concentrations[_new_state]->add_monomer();

    return 0;
}

} // namespace transitions
} // namespace stochastic
