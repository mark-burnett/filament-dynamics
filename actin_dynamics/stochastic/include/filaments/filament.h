#ifndef _STATE_FILAMENT_H_
#define _STATE_FILAMENT_H_
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

#include "state.h"
#include <deque>

// Abstract base class for filament implementations.
class Filament : private boost::noncopyable {
    public:
        virtual ~Filament() {}

        // query filament status
        virtual size_t state_count(const State &state) const = 0;
        virtual size_t boundary_count(const State &pointed_state,
                const State &barbed_state) const = 0;
        virtual size_t length() const = 0;

        // query tip states
        virtual State barbed_state() const = 0;
        virtual State pointed_state() const = 0;

        // add element to either end
        virtual void append_barbed(const State &new_state) = 0;
        virtual void append_pointed(const State &new_state) = 0;

        // remove element from either end
        virtual size_t pop_barbed() = 0;
        virtual size_t pop_pointed() = 0;

        // change nth specific state to *
        virtual void update_state(size_t instance_number,
                const State &old_states, const State &new_states) = 0;
        // change +/- element of nth specific boundary of type * to *
        virtual void update_boundary(size_t instance_number,
                const State &old_pointed_states,
                const State &old_barbed_states,
                const State &new_pointed_states,
                const State &new_barbed_states) = 0;
        virtual std::deque<State> get_states() const = 0;
};

typedef boost::shared_ptr<Filament> filament_ptr_t;
typedef std::vector< filament_ptr_t > filament_container_t;

#endif // _STATE_FILAMENT_H_
