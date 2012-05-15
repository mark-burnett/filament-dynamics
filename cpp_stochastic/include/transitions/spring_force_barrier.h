#ifndef _TRANSITIONS_SPRING_FORCE_BARRIER_
#define _TRANSITIONS_SPRING_FORCE_BARRIER_
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

#include <vector>

#include "barrier_position.h"
#include "physical_constants.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

#include "transitions/transition.h"

namespace stochastic {
namespace transitions {

class RaiseBarrierSpringForce : public Transition {
    public:
        RaiseBarrierSpringForce(double spring_constant,
                size_t zero_force_barrier_position, double D, size_t divisions):
            _rate_scale(2 * D / (std::pow(monomer_length / divisions, 2))),
            _energy_scale(spring_constant / (4 * boltzman_constant * room_temperature)),
            _barrier_dist_scale(monomer_length / divisions),
            _zero_force_barrier_position(zero_force_barrier_position) {
//                barrier_position = _zero_force_barrier_position;
            }

        double initial_R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations) {
            return _rate_scale;
        }

        double R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations,
                    size_t previous_filament_index);

        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            barrier_position++;
            return 0;
        };

    private:
        const double _rate_scale;
        const double _energy_scale;
        const double _barrier_dist_scale;
        const size_t _zero_force_barrier_position;
};

class LowerBarrierSpringForce : public Transition {
    public:
        LowerBarrierSpringForce(double spring_constant,
                size_t zero_force_barrier_position, double D, size_t divisions):
            _divisions(divisions),
            _rate_scale(2 * D / (std::pow(monomer_length / divisions, 2))),
            _energy_scale(spring_constant / (4 * boltzman_constant * room_temperature)),
            _barrier_dist_scale(monomer_length / divisions),
            _zero_force_barrier_position(zero_force_barrier_position),
            _initialized(false) {}

        double initial_R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations);

        double R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations,
                    size_t previous_filament_index);

        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            barrier_position--;
            return 0;
        }

    private:
        const size_t _divisions;
        const double _rate_scale;
        const double _energy_scale;
        const double _barrier_dist_scale;
        const size_t _zero_force_barrier_position;
        bool _initialized;

        std::vector<unsigned int> _filament_lengths;

        double _check_rate(size_t max_length);
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_SPRING_FORCE_BARRIER_
