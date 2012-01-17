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

#include <gtest/gtest.h>

#include <vector>
#include <boost/assign/std/vector.hpp>

// Bring operator+= into the namespace
using namespace boost::assign;

#include "state.h"
#include "filaments/segmented_filament.h"

TEST(SegmentedFilament, IteratorConstructor) {
    std::vector<State> values;
    values += 0, 1, 0, 0, 2, 1, 0, 1;

    SegmentedFilament f(values.begin(), values.end());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(4, f.state_count(0));
    EXPECT_EQ(3, f.state_count(1));
    EXPECT_EQ(1, f.state_count(2));
    EXPECT_EQ(2, f.boundary_count(0, 1));
    EXPECT_EQ(1, f.boundary_count(0, 2));
}

TEST(SegmentedFilament, NumberStateConstructor) {
    SegmentedFilament f(26, 0);
    EXPECT_EQ(26, f.length());
    EXPECT_EQ(26, f.state_count(0));
    EXPECT_EQ(0, f.state_count(4));
    EXPECT_EQ(0, f.barbed_state());
}

TEST(SegmentedFilament, Append) {
    SegmentedFilament f(20, 0);

    f.append_barbed(1);
    EXPECT_EQ(21, f.length());
    EXPECT_EQ(1, f.barbed_state());
    EXPECT_EQ(1, f.state_count(1));

    f.append_pointed(2);
    EXPECT_EQ(22, f.length());
    EXPECT_EQ(2, f.pointed_state());
    EXPECT_EQ(1, f.state_count(2));
}

TEST(SegmentedFilament, Remove) {
    SegmentedFilament f(20, 0);

    State s = f.pop_barbed();
    EXPECT_EQ(0, s);
    EXPECT_EQ(19, f.length());

    f.append_barbed(1);
    s = f.pop_barbed();
    EXPECT_EQ(1, s);
    EXPECT_EQ(19, f.length());

    s = f.pop_pointed();
    EXPECT_EQ(0, s);
    EXPECT_EQ(18, f.length());

    f.append_pointed(2);
    s = f.pop_pointed();
    EXPECT_EQ(2, s);
    EXPECT_EQ(18, f.length());

}

TEST(SegmentedFilament, UpdateState) {
    SegmentedFilament f(20, 0);

    f.update_state(4, 0, 1);
    EXPECT_EQ(20, f.length());
    EXPECT_EQ(1, f.state_count(1));
    EXPECT_EQ(1, f.boundary_count(0, 1));
    EXPECT_EQ(1, f.boundary_count(1, 0));

    f.update_state(3, 0, 1);
    EXPECT_EQ(2, f.state_count(1));
    EXPECT_EQ(1, f.boundary_count(0, 1));
    EXPECT_EQ(1, f.boundary_count(1, 0));

    f.update_state(1, 1, 2);
    EXPECT_EQ(1, f.state_count(1));
    EXPECT_EQ(1, f.state_count(2));
    EXPECT_EQ(1, f.boundary_count(0, 1));
    EXPECT_EQ(1, f.boundary_count(1, 2));
    EXPECT_EQ(1, f.boundary_count(2, 0));

    f.update_state(0, 0, 3);
    EXPECT_EQ(3, f.pointed_state());
    EXPECT_EQ(1, f.state_count(3));
}

/*
TEST(SegmentedFilament, UpdateBoundary) {
    SegmentedFilament f(20, 0);

    f.update_state(5, 0, 1);
    f.update_boundary(0, 0, 1, 3);
    EXPECT_EQ(1, f.boundary_count(0, 3));
    EXPECT_EQ(1, f.boundary_count(3, 0));

    f.update_state(10, 0, 3);
    EXPECT_EQ(2, f.boundary_count(0, 3));
    f.update_boundary(1, 0, 3, 4);
    EXPECT_EQ(1, f.boundary_count(0, 3));
    EXPECT_EQ(1, f.boundary_count(3, 0));
    EXPECT_EQ(1, f.boundary_count(0, 4));
    EXPECT_EQ(1, f.boundary_count(4, 0));
}
*/
