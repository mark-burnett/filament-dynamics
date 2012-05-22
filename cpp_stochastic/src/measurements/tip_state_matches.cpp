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

#include "measurements/tip_state_matches.h"

namespace stochastic {
namespace measurements {

void TipStateMatches::initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) {
    _record_once(filaments);
}

void TipStateMatches::_record_once(const filaments::container_t &filaments) {
    size_t count = 0;
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        if (filaments[fi]->barbed_state() == _state) {
            ++count;
        }
    }
    double fraction = static_cast<double>(count) / filaments.size();
    _fractions.push_back(fraction);
}

void TipStateMatches::perform(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    size_t number_to_record;
    if (sample_period > 0) {
        number_to_record = (time - previous_time) / sample_period;
    } else {
        number_to_record = 1;
    }
    for (size_t n = 0; n < number_to_record; ++n) {
        _record_once(filaments);
    }
    previous_time = (_fractions.size() - 1) * sample_period;
}


void LongestTipStateMatches::initialize(
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    _record_once(filaments);
}

void LongestTipStateMatches::_record_once(
        const filaments::container_t &filaments) {
    size_t max_length = 0;
    size_t num_longest = 0;
    size_t count = 0;
    for (size_t fi = 0; fi < filaments.size(); ++fi) {
        const size_t f_length = filaments[fi]->length();
        if (f_length > max_length) {
            max_length = f_length;
            num_longest = 1;
            count = 0;
            if (filaments[fi]->barbed_state() == _state) {
                ++count;
            }
        } else if (f_length == max_length) {
            ++num_longest;
            if (filaments[fi]->barbed_state() == _state) {
                ++count;
            }
        }
    }
    double fraction = static_cast<double>(count) / num_longest;
    _fractions.push_back(fraction);
}

void LongestTipStateMatches::perform(double time,
        const filaments::container_t &filaments,
        const concentrations::container_t &concentrations) {
    size_t number_to_record;
    if (sample_period > 0) {
        number_to_record = (time - previous_time) / sample_period;
    } else {
        number_to_record = 1;
    }
    for (size_t n = 0; n < number_to_record; ++n) {
        _record_once(filaments);
    }
    previous_time = (_fractions.size() - 1) * sample_period;
}


std::vector<double> TipStateMatches::get_times() const {
    std::vector<double> result;
    result.reserve(_fractions.size());
    result.resize(_fractions.size());
    for (size_t i = 0; i < _fractions.size(); ++i) {
        result[i] = sample_period * i;
    }
    return result;
}

std::vector<double> TipStateMatches::get_means() const {
    return _fractions;
}

std::vector<double> TipStateMatches::get_errors(
        size_t number_of_filaments) const {
    std::vector<double> result;
    result.reserve(_fractions.size());
    result.resize(_fractions.size());

    double factor = 1 / std::sqrt(number_of_filaments);

    for (size_t i = 0; i < _fractions.size(); ++i) {
        result[i] = _fractions[i] * factor;
    }

    return result;
}


std::vector<double> LongestTipStateMatches::get_times() const {
    std::vector<double> result;
    result.reserve(_fractions.size());
    result.resize(_fractions.size());
    for (size_t i = 0; i < _fractions.size(); ++i) {
        result[i] = sample_period * i;
    }
    return result;
}

std::vector<double> LongestTipStateMatches::get_means() const {
    return _fractions;
}

std::vector<double> LongestTipStateMatches::get_errors(
        size_t number_of_filaments) const {
    std::vector<double> result;
    result.reserve(_fractions.size());
    result.resize(_fractions.size());

    double factor = 1 / std::sqrt(number_of_filaments);

    for (size_t i = 0; i < _fractions.size(); ++i) {
        result[i] = _fractions[i] * factor;
    }

    return result;
}


} // namespace measurements
} // namespace stochastic
