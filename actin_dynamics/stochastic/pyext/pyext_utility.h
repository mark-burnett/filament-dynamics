#ifndef _PYEXT_UTILITY_H_
#define _PYEXT_UTILITY_H_
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

#include <vector>
#include <string>

template <typename container_type>
std::vector<std::string> get_keys(container_type &container) {
    std::vector<std::string> result;
    for (typename container_type::iterator i = container.begin();
            i != container.end(); ++i) {
        result.push_back(i->first);
    }

    return result;
}

#endif // _PYEXT_UTILITY_H_
