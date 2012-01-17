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

#include <iostream>

void SegmentedFilament::_initialize_counts() {
    _state_counts.resize(STATE_COUNT_SIZE);
    _boundary_counts.resize(STATE_COUNT_SIZE);
    for (size_t i = 0; i < STATE_COUNT_SIZE; ++i) {
        _boundary_counts[i].resize(STATE_COUNT_SIZE);
    }
}

void SegmentedFilament::_build_from_iterators(_vector_ui_ci start,
        _vector_ui_ci stop) {
    if (start == stop) {
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
    _initialize_counts();
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
    return _boundary_counts[pointed_state][barbed_state];
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
        ++_boundary_counts[_segments.back().state][new_state];
    }

    ++_length;
    ++_state_counts[new_state];
}

void SegmentedFilament::append_pointed(const State &new_state) {
    if (new_state == _segments.front().state) {
        ++_segments.front().number;
    } else {
        _segments.push_front(Segment(1, new_state));
        ++_boundary_counts[new_state][_segments.front().state];
    }

    ++_length;
    ++_state_counts[new_state];
}

State SegmentedFilament::pop_barbed() {
    Segment &seg = _segments.back();
    State state = seg.state;

    if (1 == seg.number) {
        _segments.pop_back();
        --_boundary_counts[_segments.back().state][state];
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
        --_boundary_counts[state][_segments.front().state];
    } else {
        --seg.number;
    }

    --_length;
    --_state_counts[state];

    return state;
}

void SegmentedFilament::_merge_segments(
        std::list<Segment>::iterator pointed_segment,
        std::list<Segment>::iterator target_segment,
        std::list<Segment>::iterator barbed_segment) {
    if (pointed_segment->state == target_segment->state) {
        ++pointed_segment->number;
        _segments.erase(target_segment);
        target_segment = pointed_segment;
        if (barbed_segment->state == pointed_segment->state) {
            pointed_segment->number += barbed_segment->number;
            _segments.erase(barbed_segment);
        } else {
            ++_boundary_counts[pointed_segment->state][barbed_segment->state];
        }
    } else {
        ++_boundary_counts[pointed_segment->state][target_segment->state];
        if (barbed_segment->state == target_segment->state) {
            ++barbed_segment->number;
            _segments.erase(target_segment);
        } else {
            ++_boundary_counts[target_segment->state][barbed_segment->state];
        }
    }

//    if (_segments.begin() != pointed_segment) {
//        std::list<Segment>::iterator ppsi(pointed_segment);
//        --ppsi;
//        ++_boundary_counts[ppsi->state][pointed_segment->state];
//    }
//    std::list<Segment>::iterator bbsi(barbed_segment);
//    ++bbsi;
//    if (_segments.end() != bbsi) {
//        ++_boundary_counts[barbed_segment->state][bbsi->state];
//    }
}

void SegmentedFilament::_replace_single_segment(
        std::list<Segment>::iterator target_segment,
        const State &new_state) {
    // Case of nearly empty filament
    if (1 == _segments.size()) {
        target_segment->state = new_state;
    } else {
        if (_segments.begin() != target_segment) {
            std::list<Segment>::iterator pointed_segment(target_segment);
            --pointed_segment;
            --_boundary_counts[pointed_segment->state][target_segment->state];

            std::list<Segment>::iterator barbed_segment(target_segment);
            ++barbed_segment;
            if (_segments.end() != barbed_segment) {
                std::cout << "   rsr - normal path" << std::endl;
                std::cout << "   rsr - old state = "
                    << target_segment->state << " new state = "
                    << new_state << std::endl;
                // not at the front or back
                // this is the main case
                --_boundary_counts[target_segment->state][barbed_segment->state];
                // status: currently cache has no information about this section
                //  -> so we can merge them, and just count the boundaries
                target_segment->state = new_state;
                _merge_segments(pointed_segment, target_segment, barbed_segment);
            } else {
                // at the back, only have to deal with 2
                if (new_state == pointed_segment->state) {
                    ++pointed_segment->number;
                    _segments.pop_back();
                } else {
                    target_segment->state = new_state;
                    ++_boundary_counts[pointed_segment->state][new_state];
                }
            }
        } else {
            std::list<Segment>::iterator barbed_segment(target_segment);
            ++barbed_segment;
            // at the front, only have to deal with 2
            --_boundary_counts[target_segment->state][barbed_segment->state];
            if (new_state == barbed_segment->state) {
                ++barbed_segment->number;
                _segments.pop_front();
            } else {
                target_segment->state = new_state;
                ++_boundary_counts[new_state][barbed_segment->state];
            }
        }
    }
}

void SegmentedFilament::_fracture(
        std::list<Segment>::iterator original_segment,
        size_t protomer_index, const State &new_state) {
    --_state_counts[original_segment->state];
    ++_state_counts[new_state];
    if (1 == original_segment->number) {
        std::cout << "  replace single segment" << std::endl;
        _replace_single_segment(original_segment, new_state);
    } else {
        Segment new_segment(1, new_state);
        if (0 == protomer_index) {
            // add segment on barbed side, update barbed counts & "self"
            --original_segment->number;
            _segments.insert(++original_segment, new_segment);
            // update cache
        } else if (protomer_index + 1 == original_segment->number) {
            // add segment on pointed side, update pointed counts & "self"
            --original_segment->number;
            _segments.insert(original_segment, new_segment);
            // update cache
        } else {
            std::cout << "  add 2 segments, update self" << std::endl;
            // add 2 segments, update "self" counts
            Segment pointed_segment(
                    original_segment->number - protomer_index - 1,
                    original_segment->state);
            original_segment->number = protomer_index;
            std::cout << "   segment numbers: "
                << pointed_segment.number << " "
                << new_segment.number << " "
                << original_segment->number << std::endl;
            std::cout << "   segment states: "
                << pointed_segment.state << " "
                << new_segment.state << " "
                << original_segment->state << std::endl;
            _segments.insert(original_segment, pointed_segment);
            _segments.insert(original_segment, new_segment);

            ++_boundary_counts[new_state][original_segment->state];
            ++_boundary_counts[original_segment->state][new_state];
        }
    }
}

void SegmentedFilament::update_state(size_t instance_number,
        const State &old_state, const State &new_state) {
    size_t count = 0;
    std::cout << "num segments: " << _segments.size() << std::endl;
    for (std::list<Segment>::iterator si = _segments.begin();
            si != _segments.end(); ++si) {
        std::cout << si->number << " of " << si->state << std::endl;
        if (old_state == si->state) {
            count += si->number;
        }
        std::cout << " count = " << count
            << " target " << instance_number
            << std::endl;
        if (instance_number <= count) {
            _fracture(si, count - instance_number, new_state);
            return;
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

