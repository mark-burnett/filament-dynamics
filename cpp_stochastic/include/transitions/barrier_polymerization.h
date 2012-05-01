#ifndef _TRANSITIONS_BARRIER_POLYMERIZATION_H_
#define _TRANSITIONS_BARRIER_POLYMERIZATION_H_
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

class StepFunctionBarrierBarbedEndPolymerization : public Transition {
    private:
        const State _state;
        const double _rate;
        const size_t _divisions;
    public:
        StepFunctionBarrierBarbedEndPolymerization(const State &state, double rate,
                size_t divisions) :
            _state(state), _rate(rate), _divisions(divisions) {}

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
};

class LinearFunctionBarrierBarbedEndPolymerization : public Transition {
    private:
        const State _state;
        const double _rate;
        const size_t _divisions;
        const size_t _linear_width;
        const double _slope;

        double _filament_rate(size_t length);

        std::vector<double> _filament_rates;

    public:
        LinearFunctionBarrierBarbedEndPolymerization(const State &state,
                double rate, size_t divisions, size_t linear_width) :
            _state(state), _rate(rate), _divisions(divisions),
            _linear_width(linear_width), 
            _slope(rate / (linear_width)) {}

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
};

} // namespace transitions
} // namespace stochastic

#endif // _TRANSITIONS_BARRIER_POLYMERIZATION_H_
