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
    _init_number_state(number, state);
}

SegmentedFilament::SegmentedFilament(double seed_concentration, double fnc,
        const State &state) {
    size_t number = seed_concentration / fnc;
    _init_number_state(number, state);
}

void SegmentedFilament::_init_number_state(size_t number, const State &state) {
    _state_counts[state] = number;
    _segments.push_back(Segment(number, state));
    _length = number;
}

// Simple queries about the filament state.
size_t SegmentedFilament::state_count(const State &state) const {
    _count_t::const_iterator i(_state_counts.find(state));
    if (i != _state_counts.end()) {
        return i->second;
    }
    return 0;
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
    // Handle case of single (look for joins)
    if (1 == i->number) {
        sl_t::iterator pn(i);
        --pn;
        sl_t::iterator bn(i);
        ++bn;

        if ((_segments.end() != pn) && (new_state == pn->state)) {
            ++(pn->number);
            if ((_segments.end() != bn) && (new_state == bn->state)) {
                pn->number += bn->number;
                _segments.erase(bn);
            }
            _segments.erase(i);
        } else {
            if ((_segments.end() != bn) && (new_state == bn->state)) {
                ++(bn->number);
                _segments.erase(i);
            } else {
                i->state = new_state;
            }
        }

        return;
    }

    // Non 1 length cases:
    size_t left = protomer_index;
    size_t right = i->number - protomer_index - 1;

    if (left > 0) {
        sl_t::iterator pn(i);
        --pn;
        if ((_segments.end() != pn) && (i->state == pn->state)) {
            pn->number += left;
        } else {
            _segments.insert(i, Segment(left, i->state));
        }
    }
    if (right > 0) {
        _segments.insert(i, Segment(1, new_state));
        i->number = right;
    } else {
        sl_t::iterator bn(i);
        ++bn;
        if ((_segments.end() != bn) && (new_state == bn->state)) {
            ++(bn->number);
        } else {
            _segments.insert(i, Segment(1, new_state));
        }
        _segments.erase(i);
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


void SegmentedFilament::update_boundary(size_t instance_number,
        const State &old_pointed_state, const State &old_barbed_state,
        const State &new_barbed_state) {
    size_t count = 0;
    std::list<Segment>::iterator barbed_segment(_segments.begin());
    std::list<Segment>::iterator pointed_segment(_segments.begin());
    if (!_segments.empty()) {
        ++barbed_segment;
        while (barbed_segment != _segments.end()) {
            if (old_pointed_state == pointed_segment->state &&
                    old_barbed_state == barbed_segment->state) {
                if (instance_number == count) {
                    _fracture(barbed_segment, 0, //barbed_segment->number - 1,
                            new_barbed_state);
                    return;
                }
                ++count;
            }
            ++pointed_segment;
            ++barbed_segment;
        }
    }
}

} // namespace filaments
} // namespace stochastic
