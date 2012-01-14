#ifndef _STATE_SIMPLE_FILAMENT_H_
#define _STATE_SIMPLE_FILAMENT_H_
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

#include <deque>
#include <vector>

#include "state/filament.h"

typedef std::vector<size_t>::const_iterator _vector_ui_ci;

class SimpleFilament : public Filament {
    public:
        SimpleFilament(_vector_ui_ci start, _vector_ui_ci stop);
        SimpleFilament(size_t number, size_t state);

        size_t state_count(size_t state) const;
        size_t boundary_count(size_t pointed_state,
                size_t barbed_state) const;
        size_t length() const;

        size_t barbed_state() const;
        size_t pointed_state() const;

        void append_barbed(size_t new_state);
        void append_pointed(size_t new_state);

        size_t pop_barbed();
        size_t pop_pointed();

        void update_state(size_t instance_number,
                size_t old_state, size_t new_state);
        void update_boundary(size_t instance_number,
                size_t old_pointed_state, size_t old_barbed_state,
                size_t new_pointed_state, size_t new_barbed_state);

    private:
        std::deque<size_t> states;
};

#endif // _STATE_SIMPLE_FILAMENT_H_
