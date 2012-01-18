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

namespace stochastic {
namespace filaments {

void CachedFilament::_build_from_iterators(_vector_ui_ci start,
        _vector_ui_ci stop) {
    bool first = true;
    State pointed_state;
    State barbed_state("");
    while (start < stop) {
        _states.push_back(*start);
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
    _state_counts[state] = number;
    _boundary_counts[state][state] = number - 1;
    for (size_t i = 0; i < number; ++i) {
        _states.push_back(state);
    }
}

// Cached queries about the filament state.
size_t CachedFilament::state_count(const State &state) const {
    return _state_counts.find(state)->second;
}

size_t CachedFilament::boundary_count(const State &pointed_state,
        const State &barbed_state) const {
    return _boundary_counts.find(pointed_state)->second
        .find(barbed_state)->second;
}

size_t CachedFilament::length() const {
    return _states.size();
}

State CachedFilament::barbed_state() const {
    return _states.back();
}

State CachedFilament::pointed_state() const {
    return _states.front();
}


// Add and remove subunits
void CachedFilament::append_barbed(const State &new_state) {
    State previous_state(_states.back());
    _states.push_back(new_state);
    ++_state_counts[new_state];
    ++_boundary_counts[previous_state][new_state];
}

void CachedFilament::append_pointed(const State &new_state) {
    State previous_state(_states.front());
    _states.push_front(new_state);
    ++_state_counts[new_state];
    ++_boundary_counts[new_state][previous_state];
}

State CachedFilament::pop_barbed() {
    State state = _states.back();
    _states.pop_back();
    --_state_counts[state];
    --_boundary_counts[_states.back()][state];
    return state;
}

State CachedFilament::pop_pointed() {
    State state = _states.front();
    _states.pop_front();
    --_state_counts[state];
    --_boundary_counts[state][_states.front()];
    return state;
}


// Update states
void CachedFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    size_t count = 0;
    for (std::deque<State>::iterator i = _states.begin();
            i < _states.end(); ++i) {
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
    if (i+1 < _states.end()) {
        --_boundary_counts[*i][*(i+1)];
    }
    if (i - 1 >= _states.begin()) {
        --_boundary_counts[*(i-1)][*i];
    }

    // update state
    *i = new_state;

    // add new
    ++_state_counts[*i];
        // check for ends
    if (i+1 < _states.end()) {
        ++_boundary_counts[*i][*(i+1)];
    }
    if (i - 1 >= _states.begin()) {
        ++_boundary_counts[*(i-1)][*i];
    }

}

void CachedFilament::update_boundary(size_t instance_number,
        const State &old_pointed_state, const State &old_barbed_state,
//        const State &new_pointed_state,
        const State &new_barbed_state) {
    size_t count = 0;

    std::deque<State>::iterator pointed = _states.begin();
    std::deque<State>::iterator barbed = _states.begin();
    ++barbed;
    while (barbed < _states.end()) {
        if (*pointed == old_pointed_state && *barbed == old_barbed_state) {
            if (count == instance_number) {
//                _update_state_and_cache(pointed, new_pointed_state);
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

} // namespace filaments
} // namespace stochastic
