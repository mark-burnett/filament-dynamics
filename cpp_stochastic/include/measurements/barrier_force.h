#ifndef _MEASUREMENTS_BARRIER_FORCE_H_
#define _MEASUREMENTS_BARRIER_FORCE_H_
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

#include "measurements/measurement.h"

#include "physical_constants.h"

namespace stochastic {
namespace measurements {

class BarrierForce : public Measurement {
    private:
        size_t _rest_position;
        double _k;
        std::vector<double> _values;

        double _calculate_force();
    public:
        BarrierForce(double sample_period, size_t divisions,
                size_t rest_position) :
            Measurement(sample_period),
            _rest_position(rest_position),
            _k(monomer_length / (
                    2 * boltzman_constant * room_temperature * divisions)) {}
        ~BarrierForce() {}

        void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);
        void perform(double time, const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);

        std::vector<double> get_times() const;
        std::vector<double> get_means() const;
        std::vector<double> get_errors(size_t number_of_filaments) const;
};

} // namespace measurements
} // namespace stochastic

#endif // _MEASUREMENTS_BARRIER_FORCE_H_

