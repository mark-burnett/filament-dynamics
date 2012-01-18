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

#include "concentrations/concentration.h"
#include "concentrations/fixed_concentration.h"
#include "concentrations/fixed_reagent.h"

using namespace boost::python;
using namespace stochastic::concentrations;

// XXX I do not understand why i need shared_ptr as the storage type

void concentrations_level_definitions() {
    class_<Concentration, boost::noncopyable>(
            "Concentration", no_init)
        .def("value", &Concentration::value)
        .def("add_monomer", &Concentration::add_monomer)
        .def("remove_monomer", &Concentration::remove_monomer)
        .def("monomer_count", &Concentration::monomer_count);

    class_<FixedConcentration, bases<Concentration>,
        boost::shared_ptr<FixedConcentration>,
        boost::noncopyable >("FixedConcentration", init<double>())
            .def("value", &FixedConcentration::value)
            .def("add_monomer", &FixedConcentration::add_monomer)
            .def("remove_monomer", &FixedConcentration::remove_monomer)
            .def("monomer_count", &FixedConcentration::monomer_count);

    class_<FixedReagent, bases<Concentration>,
        boost::shared_ptr<FixedReagent>,
        boost::noncopyable >("FixedReagent", init<double, double, size_t>())
            .def("value", &FixedReagent::value)
            .def("add_monomer", &FixedReagent::add_monomer)
            .def("remove_monomer", &FixedReagent::remove_monomer)
            .def("monomer_count", &FixedReagent::monomer_count);
}
