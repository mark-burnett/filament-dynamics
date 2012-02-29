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
            ++_boundary_counts[_segments.back().state][*start];
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
    std::map<State, _count_t>::const_iterator bci(_boundary_counts.find(
                pointed_state));
    if (_boundary_counts.end() != bci) {
        _count_t::const_iterator bci_2(bci->second.find(barbed_state));
        if (bci->second.end() != bci_2) {
            return bci_2->second;
        } else {
            return 0;
        }
    } else {
        return 0;
    }
}

size_t SegmentedFilament::_direct_boundary_count(const State &pointed_state,
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
        ++_boundary_counts[_segments.back().state][new_state];
        _segments.push_back(Segment(1, new_state));
    }

    ++_length;
    ++_state_counts[new_state];
}

void SegmentedFilament::append_pointed(const State &new_state) {
    if (new_state == _segments.front().state) {
        ++_segments.front().number;
    } else {
        ++_boundary_counts[new_state][_segments.front().state];
        _segments.push_front(Segment(1, new_state));
    }

    ++_length;
    ++_state_counts[new_state];
}

State SegmentedFilament::pop_barbed() {
    if (_length > 0) {
        Segment &seg = _segments.back();
        State state = seg.state;

        if (1 == seg.number) {
            _segments.pop_back();
            if (_length > 1) {
                --_boundary_counts[_segments.back().state][state];
            }
        } else {
            --seg.number;
        }

        --_length;
        --_state_counts[state];

        return state;
    }
    return State();
//    else {
//        throw DepolymerizingEmptyFilament();
//    }
}

State SegmentedFilament::pop_pointed() {
    if (_length > 0) {
        Segment &seg = _segments.front();
        State state = seg.state;

        if (1 == seg.number) {
            _segments.pop_front();
            if (_length > 1) {
                --_boundary_counts[state][_segments.front().state];
            }
        } else {
            --seg.number;
        }

        --_length;
        --_state_counts[state];

        return state;
    }
    return State();
//    else {
//        throw DepolymerizingEmptyFilament();
//    }
}

// fracture for case where segment number is 1
void SegmentedFilament::_fracture_length_one(sl_t::iterator i,
        const State &new_state) {
    sl_t::iterator pn(i);
    --pn;
    sl_t::iterator bn(i);
    ++bn;

    if (_segments.end() != pn) {
        --_boundary_counts[pn->state][i->state];
    }
    if (_segments.end() != bn) {
        --_boundary_counts[i->state][bn->state];
    }

    // cases are:
        // near pointed end
            // only segment
            // merge no boundary
            // no merge & boundary
        // near barbed end
            // merge no boundary
            // no merge & boundary
        // not near filament ends
            // merge left & boundary,
            // merge all
            // merge right & boundary,
            // no merge & 2 boundaries,

    if (_segments.end() == pn) { // near pointed end
        if (_segments.end() == bn) { // only segment
            i->state = new_state;
        } else { // check for merge right
            if (new_state == bn->state) { // merge, no boundaries
                ++(bn->number);
                _segments.erase(i);
            } else { // no merge, boundaries
                i->state = new_state;
                ++_boundary_counts[new_state][bn->state];
            }
        }
    } else if (_segments.end() == bn) { // near barbed end
        if (new_state == pn->state) { // merge, no boundaries
            ++(pn->number);
            _segments.erase(i);
        } else { // no merge, boundaries
            i->state = new_state;
            ++_boundary_counts[pn->state][new_state];
        }
    } else { // away from ends
        if (new_state == pn->state) { // merge left or all, 0 or 1 boundaries
            if (new_state == bn->state) { // merge all, 0 boundaries
                pn->number += bn->number + 1;
                _segments.erase(bn);
            } else { // merge left, 1 boundary
                ++(pn->number);
                ++_boundary_counts[pn->state][bn->state];
            }
            _segments.erase(i);
        } else if (new_state == bn->state) { // merge right, 1 boundary
            ++(bn->number);
            ++_boundary_counts[pn->state][bn->state];
            _segments.erase(i);
        } else { // no merges, 2 boundaries
            i->state = new_state;
            ++_boundary_counts[pn->state][new_state];
            ++_boundary_counts[new_state][bn->state];
        }
    }
}

void SegmentedFilament::_fracture(sl_t::iterator i,
        size_t protomer_index, const State &new_state) {
    if (1 == i->number) {
        _fracture_length_one(i, new_state);
        return;
    }

    // Non 1 length cases:
    size_t left = protomer_index;
    size_t right = i->number - protomer_index - 1;

    // cases are left edge, middle, right edge
    // left edge:  left = 0
        // check for merge, 1 or 2 boundaries
    // right edge: right = 0
        // check for merge, 1 or 2 boundaries
    // middle: left > 0 && right > 0
        // no merge, 2 boundaries

    if (0 == left) { // left edge of segment
        sl_t::iterator pn(i);
        --pn;
        if (_segments.end() != pn) { // not near pointed end of filament
            if (new_state == pn->state) { // same, no boundary
                ++(pn->number);
                --(i->number);
            } else { // different, add boundary
                --_boundary_counts[pn->state][i->state];
                _segments.insert(i, Segment(1, new_state));
                --(i->number);
                ++_boundary_counts[pn->state][new_state];
                ++_boundary_counts[new_state][i->state];
            }
        } else { // near pointed end of filament
            _segments.insert(i, Segment(1, new_state));
            --(i->number);
            ++_boundary_counts[new_state][i->state];
        }

    } else if (0 == right) { // right edge
        sl_t::iterator bn(i);
        ++bn;
        if (_segments.end() != bn) { // not near barbed end of filament
            if (new_state == bn->state) { // same, no boundary
                ++(bn->number);
                --(i->number);
            } else { // different, add boundary
                --_boundary_counts[i->state][bn->state];
                _segments.insert(bn, Segment(1, new_state));
                i->number = left;
                ++_boundary_counts[new_state][bn->state];
                ++_boundary_counts[i->state][new_state];
            }
        } else { // near barbed end of filament
            _segments.insert(bn, Segment(1, new_state));
            i->number = left;
            ++_boundary_counts[i->state][new_state];
        }

    } else { // middle
        _segments.insert(i, Segment(left, i->state));
        _segments.insert(i, Segment(1, new_state));
        i->number = right;

        ++_boundary_counts[new_state][i->state];
        ++_boundary_counts[i->state][new_state];
    }
}


void SegmentedFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    if (instance_number >= _state_counts[old_state]) {
        throw IllegalStateIndex();
    }
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
    if (instance_number >= _boundary_counts[old_pointed_state][old_barbed_state]) {
        throw IllegalBoundaryIndex();
    }
    --_state_counts[old_barbed_state];
    ++_state_counts[new_barbed_state];

    if (!_segments.empty()) {
        size_t count = 0;

        std::list<Segment>::iterator barbed_segment(_segments.begin());
        std::list<Segment>::iterator pointed_segment(_segments.begin());
        ++barbed_segment;

        if (_segments.end() == barbed_segment) {
            throw BoundaryUpdateSmallFilament();
        }

        while (barbed_segment != _segments.end()) {
            if (old_pointed_state == pointed_segment->state &&
                    old_barbed_state == barbed_segment->state) {
                if (instance_number == count) {
                    // When updating boundaries,
                    // we always choose the left-most protomer.
                    _fracture(barbed_segment, 0, new_barbed_state);
                    return;
                }
                ++count;
            }
            ++pointed_segment;
            ++barbed_segment;
        }
    } else {
        throw BoundaryUpdateEmptyFilament();
    }
}

std::vector<State> SegmentedFilament::get_states() const {
    std::vector<State> result;
    result.reserve(_length);

    for (sl_t::const_iterator seg_i = _segments.begin();
            seg_i != _segments.end(); ++seg_i) {
        for (size_t i = 0; i < seg_i->number; ++i) {
            result.push_back(seg_i->state);
        }
    }

    return result;
}

} // namespace filaments
} // namespace stochastic
