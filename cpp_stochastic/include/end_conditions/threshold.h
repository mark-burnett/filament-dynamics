#ifndef _END_CONDITIONS_THRESHOLD_H_
#define _END_CONDITIONS_THRESHOLD_H_
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

#include "end_conditions/end_condition.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

namespace stochastic {
namespace end_conditions {

class Threshold : public EndCondition {
    public:
        Threshold(const State &state, double concentration,
                double scaled_by=1,
                double subtract_fraction=0) : _state(state),
            _value(concentration * (scaled_by - subtract_fraction)) {}
        void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) {}

        bool satisfied(double time,
                const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) {
            return concentrations.find(_state)->second->value() > _value;
        }
    private:
        const State _state;
        const double _value;
};

} // namespace end_conditions
} // namespace stochastic

#endif // _END_CONDITIONS_THRESHOLD_H_
