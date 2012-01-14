#ifndef _TRANSITIONS_TRANSITION_H_
#define _TRANSITIONS_TRANSITION_H_
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

#include <boost/utility.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include "concentrations/concentration.h"
#include "filaments/filament.h"

class Transition : public boost::noncopyable {
    public:
        virtual double R(double time,
                    const filament_container_t &filaments,
                    const concentration_container_t &concentrations) = 0;
        virtual size_t perform(double time, double r,
                    filament_container_t &filaments,
                    concentration_container_t &concentrations) = 0;
};

typedef boost::ptr_vector<Transition> transition_container_t;

#endif // _TRANSITIONS_TRANSITION_H_
