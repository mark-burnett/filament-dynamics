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

#include <boost/utility.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

class Concentration : public boost::noncopyable {
    public:
        virtual double value() const = 0;
        virtual void add_monomer() = 0;
        virtual void remove_monomer() = 0;
};

typedef boost::ptr_vector<Concentration> concentration_container_t;

#endif // _CONCENTRATIONS_CONCENTRATION_H_
