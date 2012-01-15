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

#include "filaments/simple_filament.h"

#include "state.h"

SimpleFilament::SimpleFilament(_vector_ui_ci start, _vector_ui_ci stop) {
    while (start < stop) {
        states.push_back(*start);
        ++start;
    }
}

SimpleFilament::SimpleFilament(size_t number, const State &state) {
    for (size_t i = 0; i < number; ++i) {
        states.push_back(state);
    }
}

// Simple queries about the filament state.
size_t SimpleFilament::state_count(const State &state) const {
    size_t count = 0;
    for (std::deque<State>::const_iterator i = states.begin();
            i < states.end(); ++i) {
        if (*i == state) {
            ++count;
        }
    }

    return count;
}

size_t SimpleFilament::boundary_count(const State &pointed_state,
        const State &barbed_state) const {
    size_t count = 0;

    std::deque<State>::const_iterator pointed = states.begin();
    std::deque<State>::const_iterator barbed = states.begin();
    ++barbed;
    while (barbed < states.end()) {
        if (*pointed == pointed_state && *barbed == barbed_state) {
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }

    return count;
}

size_t SimpleFilament::length() const {
    return states.size();
}

State SimpleFilament::barbed_state() const {
    return states.back();
}

State SimpleFilament::pointed_state() const {
    return states.front();
}


// Add and remove subunits
void SimpleFilament::append_barbed(const State &new_state) {
    states.push_back(new_state);
}

void SimpleFilament::append_pointed(const State &new_state) {
    states.push_front(new_state);
}

State SimpleFilament::pop_barbed() {
    State state = states.back();
    states.pop_back();
    return state;
}

State SimpleFilament::pop_pointed() {
    State state = states.front();
    states.pop_front();
    return state;
}


// Update states
void SimpleFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    size_t count = 0;
    for (std::deque<State>::iterator i = states.begin();
            i < states.end(); ++i) {
        if (*i == old_state) {
            if (count == instance_number) {
                *i = new_state;
                return;
            }
            ++count;
        }
    }
}

void SimpleFilament::update_boundary(size_t instance_number,
        const State &old_pointed_state, const State &old_barbed_state,
        const State &new_pointed_state, const State &new_barbed_state) {
    size_t count = 0;

    std::deque<State>::iterator pointed = states.begin();
    std::deque<State>::iterator barbed = states.begin();
    ++barbed;
    while (barbed < states.end()) {
        if (*pointed == old_pointed_state && *barbed == old_barbed_state) {
            if (count == instance_number) {
                *pointed = new_pointed_state;
                *barbed = new_barbed_state;
            }
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }
}
