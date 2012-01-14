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

class Measurement : private boost::noncopyable {
    public:
        virtual ~Measurement() {}
};

class ConcentrationMeasurement : public Measurement {
    public:
        virtual ~ConcentrationMeasurement();
        virtual void store(double time, double value) = 0;
};

class FilamentMeasurement : public Measurement {
    public:
        virtual ~FilamentMeasurement();
        virtual void store(double time, double value,
                size_t filament_index) = 0;
};

typedef boost::shared_ptr<Measurement> measurement_ptr_t;
typedef std::vector< measurement_ptr_t > measurement_container_t;

#endif // _MEASUREMENTS_MEASUREMENT_H_
