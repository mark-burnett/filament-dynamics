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

#include "end_conditions/duration.h"
#include "end_conditions/event_count.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

TEST(EndConditions, Duration) {
    Duration ec(4.3);

    concentration_container_t concentrations;
    filament_container_t filaments;

    EXPECT_FALSE(ec.satisfied(0, filaments, concentrations));
    EXPECT_FALSE(ec.satisfied(1.3, filaments, concentrations));
    EXPECT_FALSE(ec.satisfied(4.2999, filaments, concentrations));
    EXPECT_FALSE(ec.satisfied(4.3, filaments, concentrations));
    EXPECT_TRUE(ec.satisfied(4.3001, filaments, concentrations));
    EXPECT_TRUE(ec.satisfied(8, filaments, concentrations));
}

TEST(EndConditions, EventCount) {
    EventCount ec(3);

    concentration_container_t concentrations;
    filament_container_t filaments;

    EXPECT_FALSE(ec.satisfied(0, filaments, concentrations));
    EXPECT_FALSE(ec.satisfied(1.3, filaments, concentrations));
    EXPECT_FALSE(ec.satisfied(4.2999, filaments, concentrations));
    EXPECT_TRUE(ec.satisfied(4.3, filaments, concentrations));
    EXPECT_TRUE(ec.satisfied(4.3001, filaments, concentrations));
    EXPECT_TRUE(ec.satisfied(8, filaments, concentrations));
}
