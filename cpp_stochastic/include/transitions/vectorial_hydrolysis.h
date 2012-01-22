#ifndef _TRANSITIONS_VECTORIAL_HYDROLYSIS_H_
#define _TRANSITIONS_VECTORIAL_HYDROLYSIS_H_
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

namespace stochastic {
namespace transitions {

class VectorialHydrolysis : public Transition {
    public:
        VectorialHydrolysis(const State &pointed_neighbor,
                const State &old_state, const State &new_state, double rate) :
            _pointed_neighbor(pointed_neighbor), _old_state(old_state),
            _new_state(new_state), _rate(rate), _count(0) {}
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
        const State _pointed_neighbor;
        const State _old_state;
        const State _new_state;
        const double _rate;


        // cache
        size_t _count;
        std::vector<size_t> _filament_counts;
};

class VectorialHydrolysisWithByproduct : public VectorialHydrolysis {
    public:
        VectorialHydrolysisWithByproduct(const State &pointed_neighbor,
                const State &old_state, const State &new_state,
                double rate, const State &byproduct) :
            VectorialHydrolysis(pointed_neighbor, old_state, new_state, rate),
            _byproduct(byproduct) {}

        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            concentrations[_byproduct]->add_monomer();
            return VectorialHydrolysis::perform(time, r, filaments, concentrations);
        }

    private:
        State _byproduct;
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_VECTORIAL_HYDROLYSIS_H_
