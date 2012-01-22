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

#include <vector>

#include <boost/python.hpp>

#include "state.h"

#include "filaments/filament.h"
#include "filaments/cached_filament.h"
#include "filaments/segmented_filament.h"
#include "filaments/simple_filament.h"

using namespace boost::python;
using namespace stochastic::filaments;

void filaments_level_definitions() {
    class_<Filament, boost::noncopyable>(
            "Filament", no_init)
        .def("state_count", &Filament::state_count)
        .def("boundary_count", &Filament::boundary_count)
        .def("length", &Filament::length)
        .def("barbed_state", &Filament::barbed_state)
        .def("pointed_state", &Filament::pointed_state)
        .def("append_barbed", &Filament::append_barbed)
        .def("append_pointed", &Filament::append_pointed)
        .def("pop_barbed", &Filament::pop_barbed)
        .def("pop_pointed", &Filament::pop_pointed)
        .def("update_state", &Filament::update_state)
        .def("update_boundary", &Filament::update_boundary)
        .def("get_states", &Filament::get_states);

    class_<CachedFilament, bases<Filament>,
        boost::shared_ptr<CachedFilament>, boost::noncopyable>(
            "CachedFilament", init<double, double, const stochastic::State &>())
        .def("state_count", &CachedFilament::state_count)
        .def("boundary_count", &CachedFilament::boundary_count)
        .def("length", &CachedFilament::length)
        .def("barbed_state", &CachedFilament::barbed_state)
        .def("pointed_state", &CachedFilament::pointed_state)
        .def("append_barbed", &CachedFilament::append_barbed)
        .def("append_pointed", &CachedFilament::append_pointed)
        .def("pop_barbed", &CachedFilament::pop_barbed)
        .def("pop_pointed", &CachedFilament::pop_pointed)
        .def("update_state", &CachedFilament::update_state)
        .def("update_boundary", &CachedFilament::update_boundary)
        .def("get_states", &CachedFilament::get_states);

    object segmented_filament = class_<SegmentedFilament, bases<Filament>,
        boost::shared_ptr<SegmentedFilament>, boost::noncopyable>(
                "SegmentedFilament", init<double, double,
            const stochastic::State &>())
        .def("state_count", &SegmentedFilament::state_count)
        .def("boundary_count", &SegmentedFilament::boundary_count)
        .def("length", &SegmentedFilament::length)
        .def("barbed_state", &SegmentedFilament::barbed_state)
        .def("pointed_state", &SegmentedFilament::pointed_state)
        .def("append_barbed", &SegmentedFilament::append_barbed)
        .def("append_pointed", &SegmentedFilament::append_pointed)
        .def("pop_barbed", &SegmentedFilament::pop_barbed)
        .def("pop_pointed", &SegmentedFilament::pop_pointed)
        .def("update_state", &SegmentedFilament::update_state)
        .def("update_boundary", &SegmentedFilament::update_boundary)
        .def("get_states", &SegmentedFilament::get_states);

    // Set segmented filament as the default
    scope().attr("DefaultFilament") = segmented_filament;

    class_<SimpleFilament, bases<Filament>,
        boost::shared_ptr<SimpleFilament>, boost::noncopyable>(
            "SimpleFilament", init<double, double, const stochastic::State &>())
        .def("state_count", &SimpleFilament::state_count)
        .def("boundary_count", &SimpleFilament::boundary_count)
        .def("length", &SimpleFilament::length)
        .def("barbed_state", &SimpleFilament::barbed_state)
        .def("pointed_state", &SimpleFilament::pointed_state)
        .def("append_barbed", &SimpleFilament::append_barbed)
        .def("append_pointed", &SimpleFilament::append_pointed)
        .def("pop_barbed", &SimpleFilament::pop_barbed)
        .def("pop_pointed", &SimpleFilament::pop_pointed)
        .def("update_state", &SimpleFilament::update_state)
        .def("update_boundary", &SimpleFilament::update_boundary)
        .def("get_states", &SimpleFilament::get_states);

}
