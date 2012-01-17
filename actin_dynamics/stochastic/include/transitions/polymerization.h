#ifndef _TRANSITIONS_POLYMERIZATION_H_
#define _TRANSITIONS_POLYMERIZATION_H_
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


class FixedRatePolymerization : public Transition {
    public:
        FixedRatePolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            _state(state), _rate(rate), _disable_time(disable_time) {}

        double initial_R(double time,
                    const filament_container_t &filaments,
                    const concentration_container_t &concentrations);

        double R(double time,
                    const filament_container_t &filaments,
                    const concentration_container_t &concentrations,
                    size_t previous_filament_index);

        size_t perform(double time, double r,
                    filament_container_t &filaments,
                    concentration_container_t &concentrations);

        virtual State get_state(const Filament &filament) const = 0;
        virtual void append_state(Filament &filament) = 0;

    protected:
        const State _state;

    private:
        const double _rate;
        const double _disable_time;
};

class BarbedEndPolymerization : public FixedRatePolymerization {
    public:
        BarbedEndPolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            FixedRatePolymerization(state, rate, disable_time) {}

        State get_state(const Filament &filament) const {
            return filament.barbed_state();
        }

        void append_state(Filament &filament) {
            filament.append_barbed(_state);
        }
};

class PointedEndPolymerization : public FixedRatePolymerization {
    public:
        PointedEndPolymerization(const State &state, double rate,
                double disable_time=-1.0) :
            FixedRatePolymerization(state, rate, disable_time) {}

        State get_state(const Filament &filament) const {
            return filament.pointed_state();
        }

        void append_state(Filament &filament) {
            filament.append_pointed(_state);
        }
};

#endif // _TRANSITIONS_POLYMERIZATION_H_
