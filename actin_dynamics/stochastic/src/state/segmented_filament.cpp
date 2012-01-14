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

#include "state/segmented_filament.h"


// Simple queries about the filament state.
size_t SegmentedFilament::state_count(size_t state) const {
    size_t count = 0;
    for (std::deque<Segment>::const_iterator i = segments.begin();
            i < segments.end(); ++i) {
        if (i->state == state) {
            count += i->number;
        }
    }

    return count;
}

size_t SegmentedFilament::boundary_count(size_t pointed_state,
        size_t barbed_state) const {
    count = 0;

    std::deque<Segment>::const_iterator pointed = segments.begin();
    std::deque<Segment>::const_iterator barbed = segments.begin();
    ++barbed;
    while (barbed < segments.end()) {
        if (pointed->state == pointed_state &&
                barbed->state == barbed_state) {
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }

    return count;
}

size_t SegmentedFilament::length() const {
    size_t count = 0;
    for (std::deque<Segment>::const_iterator i = segments.begin();
            i < segments.end(); ++i) {
        count += i->number;
    }

    return count;
}

size_t SegmentedFilament::barbed_state() const {
    return segments.back().state
}

size_t SegmentedFilament::pointed_state() const {
    return segments.front().state
}

// Add and remove subunits
void SegmentedFilament::append_barbed(size_t new_state){
    segments.push_back(Segment(1, new_state));
    _merge_segments(segments.rbegin(), 2)
}

void SegmentedFilament:update_state(size_t instance_number,
        size_t new_state) {
}
