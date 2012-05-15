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

#include "state.h"

#include "measurements/measurement.h"
#include "measurements/concentration.h"
#include "measurements/filament_length.h"
#include "measurements/state_count.h"
#include "measurements/barrier_position.h"
#include "measurements/barrier_force.h"

using namespace boost::python;
using namespace stochastic;
using namespace stochastic::measurements;

void measurements_level_definitions() {
    class_<Measurement, boost::shared_ptr<Measurement>,
        boost::noncopyable>("Measurement", no_init)
        .def("initialize", &Measurement::initialize)
        .def("perform",    &Measurement::perform)
        .def("get_times",  &Measurement::get_times)
        .def("get_means",  &Measurement::get_means)
        .def("get_errors",  &Measurement::get_errors);

    class_<Concentration, bases<Measurement>,
        boost::shared_ptr<Concentration>,
        boost::noncopyable>("Concentration",
                init<const State &, double>())
            .def("initialize", &Concentration::initialize)
            .def("perform",    &Concentration::perform)
            .def("get_times",  &Concentration::get_times)
            .def("get_means",  &Concentration::get_means)
            .def("get_errors",  &Concentration::get_errors);

    class_<FilamentMeasurement<size_t>, bases<Measurement>,
        boost::shared_ptr<FilamentMeasurement<size_t> >,
        boost::noncopyable>("_FilamentMeasurement_double", no_init)
            .def("initialize", &FilamentMeasurement<size_t>::initialize)
            .def("perform", &FilamentMeasurement<size_t>::perform)
            .def("get_times", &FilamentMeasurement<size_t>::get_times)
            .def("get_means", &FilamentMeasurement<size_t>::get_means)
            .def("get_errors",  &Measurement::get_errors);

    class_<FilamentLength, bases<FilamentMeasurement<size_t> >,
        boost::shared_ptr<FilamentLength>,
        boost::noncopyable>("FilamentLength", init<double>())
            .def("initialize", &FilamentLength::initialize)
            .def("perform", &FilamentLength::perform)
            .def("get_times", &FilamentLength::get_times)
            .def("get_means", &FilamentLength::get_means)
            .def("get_errors",  &Measurement::get_errors);

    class_<StateCount, bases<FilamentMeasurement<size_t> >,
        boost::shared_ptr<StateCount>,
        boost::noncopyable>("StateCount",
                init<const stochastic::State&, double>())
            .def("initialize", &StateCount::initialize)
            .def("perform", &StateCount::perform)
            .def("get_times", &StateCount::get_times)
            .def("get_means", &StateCount::get_means)
            .def("get_errors",  &Measurement::get_errors);

    class_<BarrierPosition, bases<Measurement>,
        boost::shared_ptr<BarrierPosition>,
                boost::noncopyable>("BarrierPosition", init<double>())
            .def("initialize", &BarrierPosition::initialize)
            .def("perform",    &BarrierPosition::perform)
            .def("get_times",  &BarrierPosition::get_times)
            .def("get_means",  &BarrierPosition::get_means)
            .def("get_errors",  &BarrierPosition::get_errors);

    class_<BarrierForce, bases<Measurement>,
        boost::shared_ptr<BarrierForce>,
                boost::noncopyable>("BarrierForce",
                    init<double, size_t, size_t, double>())
            .def("initialize", &BarrierForce::initialize)
            .def("perform",    &BarrierForce::perform)
            .def("get_times",  &BarrierForce::get_times)
            .def("get_means",  &BarrierForce::get_means)
            .def("get_errors",  &BarrierForce::get_errors);
}
