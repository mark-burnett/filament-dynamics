#ifndef _STATE_SEGMENTED_FILAMENT_H_
#define _STATE_SEGMENTED_FILAMENT_H_
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

#include "state/filament.h"

struct Segment {
    Segment(size_t new_number, unsigned int new_state) :
        number(new_number), state(new_state) {}

    size_t number;
    unsigned int state;
};

class SegmentedFilament : public Filament {
    public:
        SegmentedFilament();
        ~SegmentedFilament();

        size_t state_count(unsigned int state) const;
        size_t boundary_count(unsigned int pointed_state,
                unsigned int barbed_state) const;
        size_t length() const;

        unsigned int barbed_state() const;
        unsigned int pointed_state() const;

        void append_barbed(unsigned int new_state);
        void append_pointed(unsigned int new_state);

        unsigned int pop_barbed();
        unsigned int pop_pointed();

        void update_state(size_t instance_number, unsigned int new_state);
        void update_boundary(size_t instance_number,
                unsigned int new_pointed_state,
                unsigned int new_barbed_state);

    private:
        std::deque<Segment> segments;
};

#endif // _STATE_SEGMENTED_FILAMENT_H_
