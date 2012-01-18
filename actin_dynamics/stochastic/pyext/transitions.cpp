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

#include "transitions/transition.h"
#include "transitions/cooperative_hydrolysis.h"
#include "transitions/random_hydrolysis.h"
#include "transitions/vectorial_hydrolysis.h"
#include "transitions/polymerization.h"
#include "transitions/depolymerization.h"

using namespace boost::python;
using namespace stochastic;
using namespace stochastic::transitions;

void transitions_level_definitions() {
    class_<Transition, boost::noncopyable
        >("Transition", no_init)
        .def("initial_R", &Transition::initial_R)
        .def("R", &Transition::R)
        .def("perform", &Transition::perform);

    // Hydrolysis Transitions
    class_<CooperativeHydrolysis, bases<Transition>
        >("CooperativeHydrolysis", init<
                const State&, const State&, const State &,
                double, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<CooperativeHydrolysisWithByproduct, bases<CooperativeHydrolysis>
        >("CooperativeHydrolysisWithByproduct", init<
                const State&, const State&, const State&,
                double, const State&, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<RandomHydrolysis, bases<Transition>
        >("RandomHydrolysis", init<
                const State&, const State&, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<RandomHydrolysisWithByproduct, bases<RandomHydrolysis>
        >("RandomHydrolysisWithByproduct", init<
                const State&, const State&, double, const State&>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<VectorialHydrolysis, bases<Transition>
        >("VectorialHydrolysis", init<
                const State&, const State&, const State&, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<VectorialHydrolysisWithByproduct, bases<VectorialHydrolysis>
        >("VectorialHydrolysisWithByproduct", init<
                const State&, const State&, const State&,
                double, const State&>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);


    // Polymerization Transitions
    class_<FixedRatePolymerization, bases<Transition>, boost::noncopyable
        >("FixedRatePolymerization", no_init)
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<BarbedEndPolymerization, bases<FixedRatePolymerization>
        >("BarbedEndPolymerization", init<
                const State&, double, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<PointedEndPolymerization, bases<FixedRatePolymerization>
        >("PointedEndPolymerization", init<
                const State&, double, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);


    // Depolymerization Transitions
    class_<FixedRateDepolymerization, bases<Transition>, boost::noncopyable
        >("FixedRateDepolymerization", no_init)
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<BarbedEndDepolymerization, bases<FixedRateDepolymerization>
        >("BarbedEndDepolymerization", init<
                const State&, double, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);

    class_<PointedEndDepolymerization, bases<FixedRateDepolymerization>
        >("PointedEndDepolymerization", init<
                const State&, double, double>())
            .def("initial_R", &Transition::initial_R)
            .def("R", &Transition::R)
            .def("perform", &Transition::perform);
}
