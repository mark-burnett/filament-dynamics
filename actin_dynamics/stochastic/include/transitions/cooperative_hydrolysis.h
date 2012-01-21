#ifndef _TRANSITIONS_COOPERATIVE_HYDROLYSIS_H_
#define _TRANSITIONS_COOPERATIVE_HYDROLYSIS_H_
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

#include <iostream>
#include "state.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

#include "transitions/transition.h"
#include "transitions/random_hydrolysis.h"
#include "transitions/vectorial_hydrolysis.h"

namespace stochastic {
namespace transitions {

class CooperativeHydrolysis : public Transition {
    public:
        CooperativeHydrolysis(const State &pointed_state, const State &old_state,
                const State &new_state, double rate, double cooperativity=1) :
            _random_transition(old_state, new_state, rate),
            _vectorial_transition(pointed_state, old_state, new_state,
                    (cooperativity - 1) * rate) {}
        ~CooperativeHydrolysis() {}

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

    private:
        RandomHydrolysis _random_transition;
        VectorialHydrolysis _vectorial_transition;
        double _random_R;
        double _vectorial_R;
};

class CooperativeHydrolysisWithByproduct : public CooperativeHydrolysis {
    public:
        CooperativeHydrolysisWithByproduct(const State &pointed_state,
                const State &old_state, const State &new_state, double rate,
                const State &byproduct, double cooperativity=1) :
            CooperativeHydrolysis(pointed_state, old_state, new_state,
                    rate, cooperativity),
            _byproduct(byproduct) {}

        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            concentrations[_byproduct]->add_monomer();
            return CooperativeHydrolysis::perform(time, r, filaments, concentrations);
        }

    private:
        State _byproduct;
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_COOPERATIVE_HYDROLYSIS_H_
