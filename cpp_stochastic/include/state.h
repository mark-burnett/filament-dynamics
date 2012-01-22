#ifndef _STOCHASTIC_STATE_H_
#define _STOCHASTIC_STATE_H_
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

#include <string>
#include <boost/flyweight.hpp>
#include <boost/flyweight/no_locking.hpp>

namespace stochastic {

typedef boost::flyweight<std::string, boost::flyweights::no_locking> State;
// typedef std::string State;
// typedef size_t State;

} // namespace stochastic

#endif // _STOCHASTIC_STATE_H_
