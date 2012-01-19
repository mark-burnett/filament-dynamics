#ifndef _MEASUREMENTS_MEASUREMENT_H_
#define _MEASUREMENTS_MEASUREMENT_H_
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

#include <boost/shared_ptr.hpp>
#include <boost/utility.hpp>

#include "filaments/filament.h"
#include "concentrations/concentration.h"

namespace stochastic {
namespace measurements {

typedef std::vector< std::vector<size_t> > length_vector_t;

class Measurement : private boost::noncopyable {
    public:
        Measurement(double _sample_period) :
            sample_period(_sample_period), previous_time(0) {}
        virtual ~Measurement() {}
        virtual void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) = 0;
        virtual void perform(double time, const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) = 0;

        virtual length_vector_t get_values() const = 0;

        const double sample_period;
        double previous_time;
};

class ConcentrationMeasurement : public Measurement {
    public:
        ConcentrationMeasurement(double sample_period) :
            Measurement(sample_period) {}
        virtual ~ConcentrationMeasurement() {}
};

class FilamentMeasurement : public Measurement {
    public:
        FilamentMeasurement(double sample_period) :
            Measurement(sample_period) {}
        virtual ~FilamentMeasurement() {}
};

typedef boost::shared_ptr<Measurement> base_ptr_t;
typedef std::vector< base_ptr_t > container_t;

} // namespace measurements
} // namespace stochastic

#endif // _MEASUREMENTS_MEASUREMENT_H_