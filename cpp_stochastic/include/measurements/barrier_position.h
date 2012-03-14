#ifndef _MEASUREMENTS_BARRIER_POSITION_H_
#define _MEASUREMENTS_BARRIER_POSITION_H_
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

namespace stochastic {
namespace measurements {

class BarrierPosition : public Measurement {
    private:
        std::vector<double> _values;

    public:
        BarrierPosition(double sample_period) :
            Measurement(sample_period) {}
        ~BarrierPosition() {}

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

#endif // _MEASUREMENTS_BARRIER_POSITION_H_
