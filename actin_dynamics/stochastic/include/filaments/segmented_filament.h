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

#include <list>

#include "filaments/filament.h"

struct Segment {
    Segment(size_t new_number, size_t new_state) :
        number(new_number), state(new_state) {}

    size_t number;
    size_t state;
};

typedef std::vector<State>::const_iterator _vector_ui_ci;

class SegmentedFilament : public Filament {
    public:
        SegmentedFilament(const std::vector<State> &values) {
            _initialize_counts();
            _build_from_iterators(values.begin(), values.end());
        }
        SegmentedFilament(_vector_ui_ci start, _vector_ui_ci stop) {
            _initialize_counts();
            _build_from_iterators(start, stop);
        }
        SegmentedFilament(size_t number, const State &state);

        ~SegmentedFilament() {}

        size_t state_count(const State &state) const;
        size_t boundary_count(const State &pointed_state,
                const State &barbed_state) const;
        size_t length() const;

        State barbed_state() const;
        State pointed_state() const;

        void append_barbed(const State &new_state);
        void append_pointed(const State &new_state);

        State pop_barbed();
        State pop_pointed();

        void update_state(size_t instance_number,
                const State &old_state, const State &new_state);
        void update_boundary(size_t instance_number,
                const State &old_pointed_state, const State &old_barbed_state,
                const State &new_barbed_state);

        std::deque<State> get_states() const {return std::deque<State>();} // { return std::deque<State>(states); }

    private:
        static const size_t STATE_COUNT_SIZE = 10;
        void _initialize_counts();
        void _build_from_iterators(_vector_ui_ci start, _vector_ui_ci stop);
        void _merge_segments(
                std::list<Segment>::iterator pointed_segment,
                std::list<Segment>::iterator target_segment,
                std::list<Segment>::iterator barbed_segment);
        void _replace_single_segment(
                std::list<Segment>::iterator target_segment,
                const State &new_state);
        void _fracture(
                std::list<Segment>::iterator orignal_segment,
                size_t protomer_index, const State &new_state);

        std::list<Segment> _segments;

        size_t _length;
        std::vector<size_t> _state_counts;
        std::vector< std::vector<size_t> > _boundary_counts;
};

#endif // _STATE_SEGMENTED_FILAMENT_H_
