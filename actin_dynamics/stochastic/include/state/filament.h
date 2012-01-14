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


// Abstract base class for filament implementations.
class Filament {
    public:
        // query filament status
        virtual size_t state_count(size_t state) const = 0;
        virtual size_t boundary_count(size_t pointed_state,
                size_t barbed_state) const = 0;
        virtual size_t length() const = 0;

        // query tip states
        virtual size_t barbed_state() const = 0;
        virtual size_t pointed_state() const = 0;

        // add element to either end
        virtual void append_barbed(size_t new_state) = 0;
        virtual void append_pointed(size_t new_state) = 0;

        // remove element from either end
        virtual size_t pop_barbed() = 0;
        virtual size_t pop_pointed() = 0;

        // change nth specific state to *
        virtual void update_state(size_t instance_number,
                size_t old_state, size_t new_state) = 0;
        // change +/- element of nth specific boundary of type * to *
        virtual void update_boundary(size_t instance_number,
                size_t old_pointed_state,
                size_t old_barbed_state,
                size_t new_pointed_state,
                size_t new_barbed_state) = 0;
};

#endif // _STATE_FILAMENT_H_
