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


// Simple queries about the filament filaments.
size_t SegmentedFilament::filaments_count(size_t filaments) const {
    size_t count = 0;
    for (std::deque<Segment>::const_iterator i = segments.begin();
            i < segments.end(); ++i) {
        if (i->filaments == filaments) {
            count += i->number;
        }
    }

    return count;
}

size_t SegmentedFilament::boundary_count(size_t pointed_filaments,
        size_t barbed_filaments) const {
    count = 0;

    std::deque<Segment>::const_iterator pointed = segments.begin();
    std::deque<Segment>::const_iterator barbed = segments.begin();
    ++barbed;
    while (barbed < segments.end()) {
        if (pointed->filaments == pointed_filaments &&
                barbed->filaments == barbed_filaments) {
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

size_t SegmentedFilament::barbed_filaments() const {
    return segments.back().filaments
}

size_t SegmentedFilament::pointed_filaments() const {
    return segments.front().filaments
}

// Add and remove subunits
void SegmentedFilament::append_barbed(size_t new_filaments){
    segments.push_back(Segment(1, new_filaments));
    _merge_segments(segments.rbegin(), 2)
}

void SegmentedFilament:update_filaments(size_t instance_number,
        size_t new_filaments) {
}
