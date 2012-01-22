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

#include "measurements/state_count.h"

namespace stochastic {
namespace measurements {

void StateCount::initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) {
    _counts.reserve(filaments.size());
    _counts.resize(filaments.size());

    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        // XXX I could reserve and resize these right now if i knew the duration and sample time
        _counts[fi].clear();
        _counts[fi].push_back(filaments[fi]->state_count(_state));
    }

    previous_time = 0;
}

void StateCount::perform(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    size_t number_to_record;
    if (sample_period > 0) {
        number_to_record = (time - previous_time) / sample_period;
    } else {
        number_to_record = 1;
    }
    for (size_t n = 0; n < number_to_record; ++n) {
        for (size_t fi = 0; fi < filaments.size(); ++fi) {
            _counts[fi].push_back(filaments[fi]->state_count(_state));
        }
    }
    previous_time = (_counts.front().size() - 1) * sample_period;
}

} // namespace measurements
} // namespace stochastic
