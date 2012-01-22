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

#include <fstream>
#include <cstring>

namespace stochastic {

unsigned int generate_random_seed() {
    char buffer[sizeof(unsigned int)];
    unsigned int seed;

    std::ifstream f("/dev/urandom", std::ios::binary);

    f.read(buffer, sizeof(unsigned int));
    memcpy(&seed, buffer, sizeof(unsigned int));
    f.close();

    return seed;
}

} // namespace stochastic
