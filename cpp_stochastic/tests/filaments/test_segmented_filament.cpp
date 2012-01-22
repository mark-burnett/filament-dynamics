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

#include "test_states.h"

using namespace stochastic;

TEST(SegmentedFilament, IteratorConstructor) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(4, f.state_count(zero));
    EXPECT_EQ(3, f.state_count(one));
    EXPECT_EQ(1, f.state_count(two));
    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(zero, two));
}

TEST(SegmentedFilament, NumberStateConstructor) {
    filaments::SegmentedFilament f(26, zero);
    EXPECT_EQ(26, f.length());EXPECT_EQ(26, f.state_count(zero));
    EXPECT_EQ( 0, f.state_count(one));
    EXPECT_EQ( 0, f.state_count(two));
    EXPECT_EQ( 0, f.state_count(three));
    EXPECT_EQ( 0, f.state_count(four));
    EXPECT_EQ(zero, f.barbed_state());
}

TEST(SegmentedFilament, Append) {
    filaments::SegmentedFilament f(20, zero);

    f.append_barbed(one);
    EXPECT_EQ(21, f.length());
    EXPECT_EQ(one, f.barbed_state());
    EXPECT_EQ(1, f.state_count(one));

    f.append_pointed(two);
    EXPECT_EQ(22, f.length());
    EXPECT_EQ(two, f.pointed_state());
    EXPECT_EQ(1, f.state_count(two));
}

TEST(SegmentedFilament, Remove) {
    filaments::SegmentedFilament f(20, zero);

    State s = f.pop_barbed();
    EXPECT_EQ(zero, s);
    EXPECT_EQ(19, f.length());

    f.append_barbed(one);
    s = f.pop_barbed();
    EXPECT_EQ(one, s);
    EXPECT_EQ(19, f.length());

    s = f.pop_pointed();
    EXPECT_EQ(zero, s);
    EXPECT_EQ(18, f.length());

    f.append_pointed(two);
    s = f.pop_pointed();
    EXPECT_EQ(two, s);
    EXPECT_EQ(18, f.length());

}

TEST(SegmentedFilament, UpdateState) {
    filaments::SegmentedFilament f(20, zero);

    f.update_state(4, zero, one);
    EXPECT_EQ(20, f.length());
    EXPECT_EQ(1, f.state_count(one));
    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, zero));

    f.update_state(3, zero, one);
    EXPECT_EQ(20, f.length());
    EXPECT_EQ(2, f.state_count(one));
    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, zero));

    f.update_state(1, one, two);
    EXPECT_EQ(20, f.length());
    EXPECT_EQ(1, f.state_count(one));
    EXPECT_EQ(1, f.state_count(two));
    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, two));
    EXPECT_EQ(1, f.boundary_count(two, zero));

    f.update_state(0, zero, three);
    EXPECT_EQ(20, f.length());
    EXPECT_EQ(three, f.pointed_state());
    EXPECT_EQ(1, f.state_count(three));
}

TEST(SegmentedFilament, UpdateBoundary) {
    filaments::SegmentedFilament f(20, zero);

    f.update_state(5, zero, one);
    f.update_boundary(0, zero, one, three);
    EXPECT_EQ(1, f.boundary_count(zero, three));
    EXPECT_EQ(1, f.boundary_count(three, zero));

    f.update_state(10, zero, three);
    EXPECT_EQ(2, f.boundary_count(zero, three));
    f.update_boundary(1, zero, three, four);
    EXPECT_EQ(1, f.boundary_count(zero, three));
    EXPECT_EQ(1, f.boundary_count(three, zero));
    EXPECT_EQ(1, f.boundary_count(zero, four));
    EXPECT_EQ(1, f.boundary_count(four, zero));
}

// Specific SegmentedFilament cases to test
TEST(SegmentedFilament, FractureSingleCasePointedEndMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += one, one, zero, zero, two, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, zero, one);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(zero, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCasePointedEndNoMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += two, one, zero, zero, two, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, zero, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(zero, two));
    EXPECT_EQ(2, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseBarbedEndMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, two, one, zero, zero;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(2, one, zero);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(zero, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseBarbedEndNoMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, two, one, zero, two;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(2, one, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(2, f.boundary_count(zero, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseNoEndLeftMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, zero, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, two, zero);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(0, f.boundary_count(zero, two));
    EXPECT_EQ(0, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseNoEndRightMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, one, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, two, one);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(0, f.boundary_count(zero, two));
    EXPECT_EQ(0, f.boundary_count(two, one));


    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseNoEndNoMerge) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, three, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, two, three);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(0, f.boundary_count(zero, two));
    EXPECT_EQ(0, f.boundary_count(two, one));

    EXPECT_EQ(1, f.boundary_count(zero, three));
    EXPECT_EQ(1, f.boundary_count(three, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureSingleCaseNoEndMergeAll) {
    std::vector<State> values;
    values += zero, one, zero, zero, two, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, zero, zero, zero, two, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, one, zero);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(1, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(zero, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}


TEST(SegmentedFilament, FractureMultipleCaseLeftEdgeNoEndMerge) {
    std::vector<State> values;
    values += zero, one, zero, one, one, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, zero, one, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(1, one, zero);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseLeftEdgeNoEndNoMerge) {
    std::vector<State> values;
    values += zero, one, zero, one, one, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, two, one, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(1, one, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(zero, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseRightEdgeNoEndMerge) {
    std::vector<State> values;
    values += zero, one, zero, one, one, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, one, one, zero, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(3, one, zero);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseRightEdgeNoEndNoMerge) {
    std::vector<State> values;
    values += zero, one, zero, one, one, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, one, one, two, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(3, one, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, zero));

    EXPECT_EQ(0, f.boundary_count(zero, two));
    EXPECT_EQ(0, f.boundary_count(two, one));

    EXPECT_EQ(1, f.boundary_count(one, two));
    EXPECT_EQ(1, f.boundary_count(two, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseMiddle) {
    std::vector<State> values;
    values += zero, one, zero, one, one, one, zero, one;

    std::vector<State> expected_result;
    expected_result += zero, one, zero, one, two, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(2, one, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    EXPECT_EQ(0, f.boundary_count(zero, two));
    EXPECT_EQ(0, f.boundary_count(two, zero));

    EXPECT_EQ(1, f.boundary_count(one, two));
    EXPECT_EQ(1, f.boundary_count(two, one));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

/*
TEST(SegmentedFilament, FractureMultipleCaseRightEdgeBarbedEnd) {
    std::vector<State> values;
    values += zero, zero, one, one, zero, one, zero, zero;

    std::vector<State> expected_result;
    expected_result += zero, zero, one, one, zero, one, zero, one;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(4, zero, one);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(3, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseLeftEdgePointedEnd) {
    std::vector<State> values;
    values += zero, zero, one, one, zero, one, zero, zero;

    std::vector<State> expected_result;
    expected_result += one, zero, one, one, zero, one, zero, zero;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(0, zero, one);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(3, f.boundary_count(one, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseLeftEdgeBarbedEndMerge) {
    std::vector<State> values;
    values += zero, zero, one, one, zero, one, zero, zero;

    std::vector<State> expected_result;
    expected_result += zero, zero, one, one, zero, one, one, zero;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(3, zero, one);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(2, f.boundary_count(one, zero));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}

TEST(SegmentedFilament, FractureMultipleCaseLeftEdgeBarbedEndNoMerge) {
    std::vector<State> values;
    values += zero, zero, one, one, zero, one, zero, zero;

    std::vector<State> expected_result;
    expected_result += zero, zero, one, one, zero, one, two, zero;

    filaments::SegmentedFilament f(values.begin(), values.end());
    f.update_state(3, zero, two);
    std::vector<State> actual_result(f.get_states());

    EXPECT_EQ(8, f.length());
    EXPECT_EQ(8, actual_result.size());

    EXPECT_EQ(2, f.boundary_count(zero, one));
    EXPECT_EQ(1, f.boundary_count(one, zero));

    EXPECT_EQ(1, f.boundary_count(two, zero));
    EXPECT_EQ(0, f.boundary_count(zero, two));

    EXPECT_EQ(0, f.boundary_count(two, one));
    EXPECT_EQ(1, f.boundary_count(one, two));

    for (size_t i = 0; i < expected_result.size(); ++i) {
        EXPECT_EQ(expected_result[i], actual_result[i])
            << "i = " << i << std::endl;
    }
}
*/
