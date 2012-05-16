#ifndef _MEASUREMENTS_TIP_STATE_MATCHES_H_
#define _MEASUREMENTS_TIP_STATE_MATCHES_H_
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

#include "filaments/filament.h"
#include "concentrations/concentration.h"

#include "measurements/filament_measurement.h"

namespace stochastic {
namespace measurements {

class TipStateMatches : public Measurement {
    public:
        TipStateMatches(const State &state, double sample_period,
                size_t number_of_filaments) :
            Measurement(sample_period), _state(state),
            _number_filaments(number_of_filaments) {}

        void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);
        void perform(double time, const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);

        std::vector<double> get_times() const;
        std::vector<double> get_means() const;
        std::vector<double> get_errors(size_t number_of_filaments) const;

    private:
        const State _state; 
        const size_t _number_filaments;
        std::vector<double> _fractions;
};

} // namespace measurements
} // namespace stochastic

#endif // _MEASUREMENTS_TIP_STATE_MATCHES_H_
