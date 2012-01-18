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

#include "filaments/segmented_filament.h"

namespace stochastic {
namespace filaments {

void SegmentedFilament::_build_from_iterators(_vector_ui_ci start,
        _vector_ui_ci stop) {
    _state_counts.reserve(STATE_COUNT_SIZE);
    _state_counts.resize(STATE_COUNT_SIZE);
    if (start == stop) {
        _length = 0;
        return;
    }

    _segments.push_back(Segment(1, *start));
    ++_state_counts[*start];
    ++start;
    _length = 1;
    for ( ; start < stop; ++start) {
        ++_state_counts[*start];
        ++_length;
        if (*start == _segments.back().state) {
            ++_segments.back().number;
        } else {
            _segments.push_back(Segment(1, *start));
        }
    }
}

SegmentedFilament::SegmentedFilament(size_t number, const State &state) {
    _state_counts.reserve(STATE_COUNT_SIZE);
    _state_counts.resize(STATE_COUNT_SIZE);
    _state_counts[state] = number;
    _segments.push_back(Segment(number, state));
    _length = number;
}

// Simple queries about the filament state.
size_t SegmentedFilament::state_count(const State &state) const {
    return _state_counts[state];
}


size_t SegmentedFilament::boundary_count(const State &pointed_state,
        const State &barbed_state) const {
    sl_t::const_iterator barbed(_segments.begin());
    sl_t::const_iterator pointed(_segments.begin());
    ++barbed;

    size_t count = 0;
    while (barbed != _segments.end()) {
        if (pointed_state == pointed->state &&
                barbed_state == barbed->state) {
            ++count;
        }
        ++barbed;
        ++pointed;
    }
    return count;
}

size_t SegmentedFilament::length() const {
    return _length;
}

State SegmentedFilament::barbed_state() const {
    return _segments.back().state;
}

State SegmentedFilament::pointed_state() const {
    return _segments.front().state;
}

// Add and remove subunits
void SegmentedFilament::append_barbed(const State &new_state) {
    if (new_state == _segments.back().state) {
        ++_segments.back().number;
    } else {
        _segments.push_back(Segment(1, new_state));
    }

    ++_length;
    ++_state_counts[new_state];
}

void SegmentedFilament::append_pointed(const State &new_state) {
    if (new_state == _segments.front().state) {
        ++_segments.front().number;
    } else {
        _segments.push_front(Segment(1, new_state));
    }

    ++_length;
    ++_state_counts[new_state];
}

State SegmentedFilament::pop_barbed() {
    Segment &seg = _segments.back();
    State state = seg.state;

    if (1 == seg.number) {
        _segments.pop_back();
    } else {
        --seg.number;
    }

    --_length;
    --_state_counts[state];

    return state;
}

State SegmentedFilament::pop_pointed() {
    Segment &seg = _segments.front();
    State state = seg.state;

    if (1 == seg.number) {
        _segments.pop_front();
    } else {
        --seg.number;
    }

    --_length;
    --_state_counts[state];

    return state;
}

void SegmentedFilament::_fracture(sl_t::iterator i,
        size_t protomer_index, const State &new_state) {
    size_t left = protomer_index;
    size_t right = i->number - protomer_index - 1;
    if (left > 0) {
        _segments.insert(i, Segment(left, i->state));
        _segments.insert(i, Segment(1, new_state));
    } else {
        sl_t::iterator pointed_neighbor(i);
        --pointed_neighbor;
        if (new_state == pointed_neighbor->state) {
            ++pointed_neighbor->number;
        } else {
            _segments.insert(i, Segment(1, new_state));
        }
    }

    if (right > 0) {
        i->number = right;
    } else {
        sl_t::iterator pointed_neighbor(i);
        --pointed_neighbor;
        sl_t::iterator barbed_neighbor(i);
        ++barbed_neighbor;

        _segments.erase(i);

        if (pointed_neighbor->state == barbed_neighbor->state) {
            barbed_neighbor->number += pointed_neighbor->number;
            _segments.erase(pointed_neighbor);
        }

    }
}

void SegmentedFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    --_state_counts[old_state];
    ++_state_counts[new_state];

    for (sl_t::iterator i = _segments.begin();
            i != _segments.end(); ++i) {
        if (old_state == i->state) {
            if (instance_number < i->number) {
                _fracture(i, instance_number, new_state);
                return;
            }
            instance_number -= i->number;
        }
    }
}


// XXX This doesn't work at all.
void SegmentedFilament::update_boundary(size_t instance_number,
        const State &old_pointed_state, const State &old_barbed_state,
        const State &new_barbed_state) {
    size_t count = 0;
    std::list<Segment>::iterator barbed_segment(_segments.begin());
    std::list<Segment>::iterator pointed_segment(_segments.begin());
    if (!_segments.empty()) {
        ++barbed_segment;
    }

    while (barbed_segment != _segments.end()) {
        if (old_pointed_state == pointed_segment->state &&
                old_barbed_state == barbed_segment->state) {
            ++count;
            if (instance_number == count) {
                _fracture(barbed_segment, barbed_segment->number - 1,
                        new_barbed_state);
                return;
            }
        }
    }
}

} // namespace filaments
} // namespace stochastic
