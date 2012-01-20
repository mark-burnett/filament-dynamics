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
#include "transitions/association.h"
#include "transitions/cooperative_hydrolysis.h"
#include "transitions/monomer.h"
#include "transitions/polymerization.h"
#include "transitions/depolymerization.h"
#include "transitions/random_hydrolysis.h"
#include "transitions/tip_hydrolysis.h"
#include "transitions/vectorial_hydrolysis.h"

using namespace boost::python;
using namespace stochastic;
using namespace stochastic::transitions;

void transitions_level_definitions() {
    class_<Transition, boost::noncopyable
        >("Transition", no_init)
        .def("initial_R", &Transition::initial_R)
        .def("R", &Transition::R)
        .def("perform", &Transition::perform);

    // Concentration-based Transitions
    class_<Association, bases<Transition>
        >("Association", init<
                const State&, const State&, const State &, double>())
            .def("initial_R", &Association::initial_R)
            .def("R", &Association::R)
            .def("perform", &Association::perform);

    class_<Monomer, bases<Transition>
        >("Monomer", init<
                const State&, const State&, double>())
            .def("initial_R", &Monomer::initial_R)
            .def("R", &Monomer::R)
            .def("perform", &Monomer::perform);

    class_<MonomerWithByproduct, bases<Monomer>
        >("MonomerWithByproduct", init<
                const State&, const State&, double, const State &>())
            .def("initial_R", &MonomerWithByproduct::initial_R)
            .def("R", &MonomerWithByproduct::R)
            .def("perform", &MonomerWithByproduct::perform);


    // Hydrolysis Transitions
    class_<CooperativeHydrolysis, bases<Transition>
        >("CooperativeHydrolysis", init<
                const State&, const State&, const State &,
                double, double>())
            .def("initial_R", &CooperativeHydrolysis::initial_R)
            .def("R", &CooperativeHydrolysis::R)
            .def("perform", &CooperativeHydrolysis::perform);

    class_<CooperativeHydrolysisWithByproduct, bases<CooperativeHydrolysis>
        >("CooperativeHydrolysisWithByproduct", init<
                const State&, const State&, const State&,
                double, const State&, double>())
            .def("initial_R", &CooperativeHydrolysisWithByproduct::initial_R)
            .def("R", &CooperativeHydrolysisWithByproduct::R)
            .def("perform", &CooperativeHydrolysisWithByproduct::perform);

    class_<RandomHydrolysis, bases<Transition>
        >("RandomHydrolysis", init<
                const State&, const State&, double>())
            .def("initial_R", &RandomHydrolysis::initial_R)
            .def("R", &RandomHydrolysis::R)
            .def("perform", &RandomHydrolysis::perform);

    class_<RandomHydrolysisWithByproduct, bases<Transition>
        >("RandomHydrolysisWithByproduct", init<
                const State&, const State&, double, const State&>())
            .def("initial_R", &RandomHydrolysisWithByproduct::initial_R)
            .def("R", &RandomHydrolysisWithByproduct::R)
            .def("perform", &RandomHydrolysisWithByproduct::perform);

    class_<VectorialHydrolysis, bases<Transition>
        >("VectorialHydrolysis", init<
                const State&, const State&, const State&, double>())
            .def("initial_R", &VectorialHydrolysis::initial_R)
            .def("R", &VectorialHydrolysis::R)
            .def("perform", &VectorialHydrolysis::perform);

    class_<VectorialHydrolysisWithByproduct, bases<Transition>
        >("VectorialHydrolysisWithByproduct", init<
                const State&, const State&, const State&,
                double, const State&>())
            .def("initial_R", &VectorialHydrolysisWithByproduct::initial_R)
            .def("R", &VectorialHydrolysisWithByproduct::R)
            .def("perform", &VectorialHydrolysisWithByproduct::perform);

    class_<TipHydrolysis, bases<Transition>, boost::noncopyable
        >("TipHydrolysis", no_init)
            .def("initial_R", &TipHydrolysis::initial_R)
            .def("R", &TipHydrolysis::R)
            .def("perform", &TipHydrolysis::perform);

    class_<BarbedTipHydrolysis, bases<TipHydrolysis>
        >("BarbedTipHydrolysis", init<const State&, const State&, double>())
            .def("initial_R", &BarbedTipHydrolysis::initial_R)
            .def("R", &BarbedTipHydrolysis::R)
            .def("perform", &BarbedTipHydrolysis::perform);

    class_<PointedTipHydrolysis, bases<TipHydrolysis>
        >("PointedTipHydrolysis", init<const State&, const State&, double>())
            .def("initial_R", &PointedTipHydrolysis::initial_R)
            .def("R", &PointedTipHydrolysis::R)
            .def("perform", &PointedTipHydrolysis::perform);

    class_<BarbedTipHydrolysisWithByproduct, bases<TipHydrolysis>
        >("BarbedTipHydrolysisWithByproduct",
                init<const State&, const State&, double, const State&>())
            .def("initial_R", &BarbedTipHydrolysisWithByproduct::initial_R)
            .def("R", &BarbedTipHydrolysisWithByproduct::R)
            .def("perform", &BarbedTipHydrolysisWithByproduct::perform);

    class_<PointedTipHydrolysisWithByproduct, bases<TipHydrolysis>
        >("PointedTipHydrolysisWithByproduct",
                init<const State&, const State&, double, const State&>())
            .def("initial_R", &PointedTipHydrolysisWithByproduct::initial_R)
            .def("R", &PointedTipHydrolysisWithByproduct::R)
            .def("perform", &PointedTipHydrolysisWithByproduct::perform);

    // Polymerization Transitions
    class_<FixedRatePolymerization, bases<Transition>, boost::noncopyable
        >("FixedRatePolymerization", no_init)
            .def("initial_R", &FixedRatePolymerization::initial_R)
            .def("R", &FixedRatePolymerization::R)
            .def("perform", &FixedRatePolymerization::perform);

    class_<BarbedEndPolymerization, bases<FixedRatePolymerization>
        >("BarbedEndPolymerization", init<
                const State&, double, double>())
            .def("initial_R", &BarbedEndPolymerization::initial_R)
            .def("R", &BarbedEndPolymerization::R)
            .def("perform", &BarbedEndPolymerization::perform);

    class_<PointedEndPolymerization, bases<FixedRatePolymerization>
        >("PointedEndPolymerization", init<
                const State&, double, double>())
            .def("initial_R", &PointedEndPolymerization::initial_R)
            .def("R", &PointedEndPolymerization::R)
            .def("perform", &PointedEndPolymerization::perform);


    // Depolymerization Transitions
    class_<FixedRateDepolymerization, bases<Transition>, boost::noncopyable
        >("FixedRateDepolymerization", no_init)
            .def("initial_R", &FixedRateDepolymerization::initial_R)
            .def("R", &FixedRateDepolymerization::R)
            .def("perform", &FixedRateDepolymerization::perform);

    class_<BarbedEndDepolymerization, bases<FixedRateDepolymerization>
        >("BarbedEndDepolymerization", init<
                const State&, double, double>())
            .def("initial_R", &BarbedEndDepolymerization::initial_R)
            .def("R", &BarbedEndDepolymerization::R)
            .def("perform", &BarbedEndDepolymerization::perform);

    class_<PointedEndDepolymerization, bases<FixedRateDepolymerization>
        >("PointedEndDepolymerization", init<
                const State&, double, double>())
            .def("initial_R", &PointedEndDepolymerization::initial_R)
            .def("R", &PointedEndDepolymerization::R)
            .def("perform", &PointedEndDepolymerization::perform);
}
