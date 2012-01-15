#ifndef _TRANSITIONS_RANDOM_HYDROLYSIS_H_
#define _TRANSITIONS_RANDOM_HYDROLYSIS_H_
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

#include "concentrations/concentration.h"
#include "filaments/filament.h"

#include "transitions/transition.h"


class RandomHydrolysis : public Transition {
    public:
        RandomHydrolysis(const State &_old_state, const State &_new_state,
                double _rate) : old_state(_old_state),
                                new_state(_new_state),
                                rate(_rate), count(0) {}
        double R(double time,
                    const filament_container_t &filaments,
                    const concentration_container_t &concentrations);
        size_t perform(double time, double r,
                    filament_container_t &filaments,
                    concentration_container_t &concentrations);

    private:
        const State old_state;
        const State new_state;
        const double rate;

        size_t count;

        // cache
        double previous_R;
        std::vector<double> filament_Rs;
};

class RandomHydrolysisWithByproduct : public RandomHydrolysis {
    public:
        RandomHydrolysisWithByproduct(const State &old_state,
                const State &new_state,
                double rate, const State &byproduct) :
            RandomHydrolysis(old_state, new_state, rate),
            _byproduct(byproduct) {}

        size_t perform(double time, double r,
                    filament_container_t &filaments,
                    concentration_container_t &concentrations) {
            concentrations[_byproduct]->add_monomer();
            return RandomHydrolysis::perform(time, r, filaments, concentrations);
        }

    private:
        State _byproduct;
};

#endif // _TRANSITIONS_RANDOM_HYDROLYSIS_H_
