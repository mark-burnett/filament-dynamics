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

#include <boost/python.hpp>

#include "measurements/measurement.h"
#include "measurements/filament_length.h"
#include "measurements/state_count.h"

using namespace boost::python;
using namespace stochastic::measurements;

void measurements_level_definitions() {
    class_<Measurement, boost::noncopyable>("Measurement", no_init)
        .def("initialize", &Measurement::initialize)
        .def("perform", &Measurement::perform)
        .def("get_values", &Measurement::get_values);
//        .def_readonly("sample_period", &Measurement::sample_period)
//        .def_readonly("previous_time", &Measurement::previous_time);

    class_<FilamentLength, bases<Measurement>,
        boost::shared_ptr<FilamentLength>,
        boost::noncopyable>("FilamentLength", init<double>())
            .def("initialize", &FilamentLength::initialize)
            .def("perform", &FilamentLength::perform)
            .def("get_values", &FilamentLength::get_values);
//            .def_readonly("sample_period", &FilamentLength::sample_period)
//            .def_readonly("previous_time", &FilamentLength::previous_time);

    class_<StateCount, bases<Measurement>,
        boost::shared_ptr<StateCount>,
        boost::noncopyable>("StateCount",
                init<const stochastic::State&, double>())
            .def("initialize", &StateCount::initialize)
            .def("perform", &StateCount::perform)
            .def("get_values", &StateCount::get_values);
//            .def_readonly("sample_period", &StateCount::sample_period)
//            .def_readonly("previous_time", &StateCount::previous_time);;
}
