#ifndef _CONCENTRATIONS_CONCENTRATION_H_
#define _CONCENTRATIONS_CONCENTRATION_H_
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

#include <map>
#include <boost/shared_ptr.hpp>

#include "state.h"

namespace stochastic {
namespace concentrations {

class Concentration {
    public:
        virtual ~Concentration() {}
        virtual double value() const { return 0; }
        virtual void add_monomer() {}
        virtual void remove_monomer() {}
        virtual size_t monomer_count() { return 0; }
        typedef boost::shared_ptr<Concentration> ptr_t;
};

typedef Concentration ZeroConcentration;

typedef std::map<State, Concentration::ptr_t> container_t;

} // namespace concentrations
} // namespace stochastic

#endif // _CONCENTRATIONS_CONCENTRATION_H_
