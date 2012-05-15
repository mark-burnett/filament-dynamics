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

#include "barrier_position.h"
#include "measurements/barrier_force.h"

namespace stochastic {
namespace measurements {

void BarrierForce::initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) {
    previous_time = 0;
    _values.clear();
    _values.push_back(_calculate_force());
}

void BarrierForce::perform(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    size_t number_to_record;
    if (sample_period > 0) {
        number_to_record = (time - previous_time) / sample_period;
    } else {
        number_to_record = 1;
    }
    for (size_t n = 0; n < number_to_record; ++n) {
        _values.push_back(_calculate_force());
    }
    previous_time = (_values.size() - 1) * sample_period;
}

double BarrierForce::_calculate_force() {
    // Note: our sign convention is that toward the bundle is positive.
    return (_k * barrier_position - _k * _rest_position);
}

std::vector<double> BarrierForce::get_times() const {
    std::vector<double> result;
    result.reserve(_values.size());
    result.resize(_values.size());
    for (size_t i = 0; i < _values.size(); ++i) {
        result[i] = sample_period * i;
    }
    return result;
}

std::vector<double> BarrierForce::get_means() const {
    return _values;
}

std::vector<double> BarrierForce::get_errors(
        size_t number_of_filaments) const {
    std::vector<double> result;
    result.reserve(_values.size());
    result.resize(_values.size());

    double factor = 1 / std::sqrt(number_of_filaments);

    for (size_t i = 0; i < _values.size(); ++i) {
        result[i] = _values[i] * factor;
    }

    return result;
}

} // namespace measurements
} // namespace stochastic
