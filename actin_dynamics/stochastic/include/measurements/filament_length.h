#ifndef _MEASUREMENTS_FILAMENT_LENGTH_H_
#define _MEASUREMENTS_FILAMENT_LENGTH_H_
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

class FilamentLength : public FilamentMeasurement {
    public:
        FilamentLength(double sample_period) :
            FilamentMeasurement(sample_period) {}

        void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);
        void perform(double time, const filaments::container_t &filaments,
                const concentrations::container_t &concentrations);

        length_vector_t get_values() const {
            return _lengths;
        }

    private:
        length_vector_t _lengths;
};

} // namespace measurements
} // namespace stochastic

#endif // _MEASUREMENTS_FILAMENT_LENGTH_H_
