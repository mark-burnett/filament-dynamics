#ifndef _TRANSITIONS_DEPOLYMERIZATION_H_
#define _TRANSITIONS_DEPOLYMERIZATION_H_
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

#include "state.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

#include "transitions/transition.h"

namespace stochastic {
namespace transitions {

class FixedRateDepolymerization : public Transition {
    public:
        FixedRateDepolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            _state(state), _rate(rate), _disable_time(disable_time), _count(0) {}

        double initial_R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations);

        double R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations,
                    size_t previous_filament_index);

        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations);

        virtual State get_state(const filaments::Filament &filament) const = 0;
        virtual State remove_state(filaments::Filament &filament) = 0;

    private:
        const State _state;
        const double _rate;
        const double _disable_time;
        size_t _count;
        std::vector<State> _states;
};

class BarbedEndDepolymerization : public FixedRateDepolymerization {
    public:
        BarbedEndDepolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            FixedRateDepolymerization(state, rate, disable_time) {}

        State get_state(const filaments::Filament &filament) const {
            return filament.barbed_state();
        }

        State remove_state(filaments::Filament &filament) {
            return filament.pop_barbed();
        }
};

class PointedEndDepolymerization : public FixedRateDepolymerization {
    public:
        PointedEndDepolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            FixedRateDepolymerization(state, rate, disable_time) {}

        State get_state(const filaments::Filament &filament) const {
            return filament.pointed_state();
        }

        State remove_state(filaments::Filament &filament) {
            return filament.pop_pointed();
        }
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_DEPOLYMERIZATION_H_
