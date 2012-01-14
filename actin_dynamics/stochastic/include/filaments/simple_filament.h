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
#include <boost/utility.hpp>

#include "state.h"
#include "filaments/filament.h"

typedef std::vector<State>::const_iterator _vector_ui_ci;

class SimpleFilament : public Filament {
    public:
        SimpleFilament(_vector_ui_ci start, _vector_ui_ci stop);
        SimpleFilament(size_t number, State state);

        size_t state_count(State state) const;
        size_t boundary_count(State pointed_state,
                State barbed_state) const;
        size_t length() const;

        State barbed_state() const;
        State pointed_state() const;

        void append_barbed(State new_state);
        void append_pointed(State new_state);

        State pop_barbed();
        State pop_pointed();

        void update_state(size_t instance_number,
                State old_state, State new_state);
        void update_boundary(size_t instance_number,
                State old_pointed_state, State old_barbed_state,
                State new_pointed_state, State new_barbed_state);

    private:
        std::deque<State> states;
};

#endif // _STATE_SIMPLE_FILAMENT_H_
