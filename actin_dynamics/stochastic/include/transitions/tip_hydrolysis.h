#ifndef _TRANSITIONS_TIP_HYDROLYSIS_H_
#define _TRANSITIONS_TIP_HYDROLYSIS_H_
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

class TipHydrolysis : public Transition {
    public:
        TipHydrolysis(const State &old_state,
                const State &new_state, double rate):
            _new_state(new_state), _old_state(old_state), _rate(rate),
            _count(0) {}

        double initial_R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations);

        double R(double time,
                    const filaments::container_t &filaments,
                    const concentrations::container_t &concentrations,
                    size_t previous_filament_index);

        virtual size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations);

        virtual State get_state(const filaments::Filament &filament) const = 0;
        virtual void perform_filament(filaments::Filament &filament) = 0;

    protected:
        const State _new_state;
    private:
        const State _old_state;
        const double _rate;
        size_t _count;
        std::vector<State> _states;
};

class BarbedTipHydrolysis : public TipHydrolysis {
    public:
        BarbedTipHydrolysis(const State &old_state,
                const State &new_state, double rate):
            TipHydrolysis(old_state, new_state, rate) {}

        State get_state(const filaments::Filament &filament) const {
            return filament.barbed_state();
        }

        void perform_filament(filaments::Filament &filament) {
            filament.pop_barbed();
            filament.append_barbed(_new_state);
        }
};

class PointedTipHydrolysis : public TipHydrolysis {
    public:
        PointedTipHydrolysis(const State &old_state,
                const State &new_state, double rate):
            TipHydrolysis(old_state, new_state, rate) {}

        State get_state(const filaments::Filament &filament) const {
            return filament.pointed_state();
        }

        void perform_filament(filaments::Filament &filament) {
            filament.pop_pointed();
            filament.append_pointed(_new_state);
        }
};

class BarbedTipHydrolysisWithByproduct : public BarbedTipHydrolysis {
    public:
        BarbedTipHydrolysisWithByproduct(const State &old_state,
                const State &new_state, double rate, const State &byproduct):
            BarbedTipHydrolysis(old_state, new_state, rate),
            _byproduct(byproduct) {}
        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            concentrations[_byproduct]->add_monomer();
            return BarbedTipHydrolysis::perform(time, r,
                    filaments, concentrations);
        }

    private:
        State _byproduct;
};

class PointedTipHydrolysisWithByproduct : public PointedTipHydrolysis {
    public:
        PointedTipHydrolysisWithByproduct(const State &old_state,
                const State &new_state, double rate, const State &byproduct):
            PointedTipHydrolysis(old_state, new_state, rate),
            _byproduct(byproduct) {}
        size_t perform(double time, double r,
                    filaments::container_t &filaments,
                    concentrations::container_t &concentrations) {
            concentrations[_byproduct]->add_monomer();
            return PointedTipHydrolysis::perform(time, r,
                    filaments, concentrations);
        }

    private:
        State _byproduct;
};

// typedef WithByproduct<BarbedTipHydrolysis>
//     BarbedTipHydrolysisWithByproduct;
// typedef WithByproduct<PointedTipHydrolysis>
//     PointedTipHydrolysisWithByproduct;

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_TIP_HYDROLYSIS_H_
