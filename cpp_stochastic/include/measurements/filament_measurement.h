#ifndef _MEASUREMENTS_FILAMENT_MEASUREMENT_H_
#define _MEASUREMENTS_FILAMENT_MEASUREMENT_H_
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

#include <algorithm>
#include <cmath>
#include "measurements/measurement.h"

namespace stochastic {
namespace measurements {

template <typename value_type>
class FilamentMeasurement : public Measurement {
    public:
        FilamentMeasurement(double sample_period) :
            Measurement(sample_period) {}
        virtual ~FilamentMeasurement() {}

        typedef typename std::vector< std::vector<value_type> > result_type;

        std::vector<double> get_times() const {
            result_type values = get_values();
            std::vector<double> results;
            if (!values.empty()) {
                size_t num_samples = values[0].size();
                results.reserve(num_samples);
                results.resize(num_samples);
                for (size_t i = 0; i < num_samples; ++i) {
                    results[i] = i * sample_period;
                }
            }
            return results;
        }

        std::vector<double> get_means() const {
            result_type values = get_values();
            std::vector<double> results;
            if (!values.empty()) {
                const size_t num_filaments = values.size();
                const size_t num_samples = values[0].size();
                results.reserve(num_samples);
                results.resize(num_samples);
                for (size_t si = 0; si < num_samples; ++si) {
                    value_type total = 0;
                    for (size_t fi = 0; fi < num_filaments; ++fi) {
                        total += values[fi][si];
                    }
                    results[si] = static_cast<double>(total) / num_filaments;
                }
            }
            return results;
        }

        std::vector<double> get_errors(size_t number_of_filaments) const {

            std::vector<double> means = get_means();
            std::vector<double> results;

            result_type values = get_values();
            if (!values.empty()) {
                const size_t num_filaments = values.size();
                const size_t num_samples = values[0].size();

                double factor = static_cast<double>(1) / (
                        std::max(num_filaments, (size_t)2) - 1);

                results.reserve(num_samples);
                results.resize(num_samples);
                for (size_t si = 0; si < num_samples; ++si) {
                    double total = 0;
                    for (size_t fi = 0; fi < num_filaments; ++fi) {
                        total += std::pow((values[fi][si] - means[si]), 2);
                    }
                    results[si] = factor * std::sqrt(total);
                }
            }
            return results;
        }

        virtual result_type get_values() const = 0;
};

} // namespace measurements
} // namespace stochastic

#endif // _MEASUREMENTS_FILAMENT_MEASUREMENT_H_
