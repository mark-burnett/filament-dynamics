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

#include "concentrations/fixed_concentration.h"
#include "concentrations/fixed_reagent.h"


TEST(Concentrations, FixedConcentration) {
    stochastic::concentrations::FixedConcentration c(3.1);

    EXPECT_DOUBLE_EQ(3.1, c.value());

    c.remove_monomer();
    EXPECT_DOUBLE_EQ(3.1, c.value());

    c.add_monomer();
    EXPECT_DOUBLE_EQ(3.1, c.value());
}

TEST(Concentrations, FixedReagent) {
    stochastic::concentrations::FixedReagent c(4.8, 1.2);

    EXPECT_DOUBLE_EQ(4.8, c.value());

    c.remove_monomer();
    EXPECT_DOUBLE_EQ(3.6, c.value());

    c.add_monomer();
    c.add_monomer();

    EXPECT_DOUBLE_EQ(6, c.value());
}
