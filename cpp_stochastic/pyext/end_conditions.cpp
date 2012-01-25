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

#include "end_conditions/end_condition.h"
#include "end_conditions/duration.h"
#include "end_conditions/event_count.h"
#include "end_conditions/threshold.h"

using namespace boost::python;
using namespace stochastic::end_conditions;

void end_conditions_level_definitions() {
    class_<EndCondition, boost::noncopyable>(
            "EndCondition", no_init)
        .def("initialize", &EndCondition::initialize)
        .def("satisfied", &EndCondition::satisfied);

    class_<Duration, bases<EndCondition>,
        boost::shared_ptr<Duration>,
        boost::noncopyable >("Duration", init<double>())
            .def("initialize", &Duration::initialize)
            .def("satisfied", &Duration::satisfied);

    class_<EventCount, bases<EndCondition>,
        boost::shared_ptr<EventCount>,
        boost::noncopyable >("EventCount", init<size_t>())
            .def("initialize", &EventCount::initialize)
            .def("satisfied", &EventCount::satisfied);

    class_<Threshold, bases<EndCondition>,
        boost::shared_ptr<Threshold>,
        boost::noncopyable >("Threshold",
                init<const stochastic::State&, double, double, double>())
            .def("initialize", &Threshold::initialize)
            .def("satisfied", &Threshold::satisfied);
}
