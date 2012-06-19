#ifndef _TRANSITIONS_ASSOCIATION_H_
#define _TRANSITIONS_ASSOCIATION_H_
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

class Association : public Transition {
    public:
        Association(const State &associating_state, const State &old_state,
                const State &new_state, double rate):
            _associating_state(associating_state), _new_state(new_state),
            _old_state(old_state), _rate(rate), _count(0) {}

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
        const State _associating_state;
        const State _new_state;
        const State _old_state;
        const double _rate;
        size_t _count;
        std::vector<size_t> _filament_counts;
};

class BarbedEndAssociation : public Transition {
    public:
        BarbedEndAssociation(
                const State &associating_state, const State &old_state,
                const State &new_state, double rate):
            _associating_state(associating_state), _new_state(new_state),
            _old_state(old_state), _rate(rate) {}

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
        const State _associating_state;
        const State _new_state;
        const State _old_state;
        const double _rate;
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_ASSOCIATION_H_
