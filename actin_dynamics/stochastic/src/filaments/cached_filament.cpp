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

#include "filaments/cached_filament.h"

#include "state.h"

void CachedFilament::_initialize_counts() {
    _state_counts.resize(STATE_COUNT_SIZE);
    _boundary_counts.resize(STATE_COUNT_SIZE);
    for (size_t i = 0; i < STATE_COUNT_SIZE; ++i) {
        _boundary_counts[i].resize(STATE_COUNT_SIZE);
    }
}


void CachedFilament::_build_from_iterators(_vector_ui_ci start, _vector_ui_ci stop) {
    bool first = true;
    State pointed_state;
    State barbed_state = 0;
    while (start < stop) {
        states.push_back(*start);
        pointed_state = barbed_state;
        barbed_state = *start;
        ++_state_counts[barbed_state];
        if (!first) {
            ++_boundary_counts[pointed_state][barbed_state];
        }
        ++start;
        first = false;
    }
}

CachedFilament::CachedFilament(size_t number, const State &state) {
    _initialize_counts();
    _state_counts[state] = number;
    _boundary_counts[state][state] = number - 1;
    for (size_t i = 0; i < number; ++i) {
        states.push_back(state);
    }
}

// Cached queries about the filament state.
size_t CachedFilament::state_count(const State &state) const {
    return _state_counts[state];
}
/*
    size_t count = 0;
    for (std::deque<State>::const_iterator i = states.begin();
            i < states.end(); ++i) {
        if (*i == state) {
            ++count;
        }
    }

    return count;
}
*/

size_t CachedFilament::boundary_count(const State &pointed_state,
        const State &barbed_state) const {
    return _boundary_counts[pointed_state][barbed_state];
}
/*
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
*/

size_t CachedFilament::length() const {
    return states.size();
}

State CachedFilament::barbed_state() const {
    return states.back();
}

State CachedFilament::pointed_state() const {
    return states.front();
}


// Add and remove subunits
void CachedFilament::append_barbed(const State &new_state) {
    State previous_state(states.back());
    states.push_back(new_state);
    ++_state_counts[new_state];
    ++_boundary_counts[previous_state][new_state];
}

void CachedFilament::append_pointed(const State &new_state) {
    State previous_state(states.front());
    states.push_front(new_state);
    ++_state_counts[new_state];
    ++_boundary_counts[new_state][previous_state];
}

State CachedFilament::pop_barbed() {
    State state = states.back();
    states.pop_back();
    --_state_counts[state];
    --_boundary_counts[states.back()][state];
    return state;
}

State CachedFilament::pop_pointed() {
    State state = states.front();
    states.pop_front();
    --_state_counts[state];
    --_boundary_counts[state][states.front()];
    return state;
}


// Update states
void CachedFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    size_t count = 0;
    for (std::deque<State>::iterator i = states.begin();
            i < states.end(); ++i) {
        if (*i == old_state) {
            if (count == instance_number) {
                _update_state_and_cache(i, new_state);
                return;
            }
            ++count;
        }
    }
}

void CachedFilament::_update_state_and_cache(std::deque<State>::iterator &i,
        State new_state) {
    // remove old
    --_state_counts[*i];
    if (i+1 < states.end()) {
        --_boundary_counts[*i][*(i+1)];
    }
    if (i - 1 >= states.begin()) {
        --_boundary_counts[*(i-1)][*i];
    }

    // update state
    *i = new_state;

    // add new
    ++_state_counts[*i];
        // check for ends
    if (i+1 < states.end()) {
        ++_boundary_counts[*i][*(i+1)];
    }
    if (i - 1 >= states.begin()) {
        ++_boundary_counts[*(i-1)][*i];
    }

}

void CachedFilament::update_boundary(size_t instance_number,
        const State &old_pointed_state, const State &old_barbed_state,
        const State &new_pointed_state, const State &new_barbed_state) {
    size_t count = 0;

    std::deque<State>::iterator pointed = states.begin();
    std::deque<State>::iterator barbed = states.begin();
    ++barbed;
    while (barbed < states.end()) {
        if (*pointed == old_pointed_state && *barbed == old_barbed_state) {
            if (count == instance_number) {
                _update_state_and_cache(pointed, new_pointed_state);
                _update_state_and_cache(barbed, new_barbed_state);
            }
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }
}
