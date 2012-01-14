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

#include <vector>

#include <boost/shared_ptr.hpp>
#include <boost/utility.hpp>

class Concentration : private boost::noncopyable {
    public:
        virtual ~Concentration() {};
        virtual double value() const = 0;
        virtual void add_monomer() = 0;
        virtual void remove_monomer() = 0;
};

typedef boost::shared_ptr<Concentration> concentration_ptr_t;
typedef std::vector< concentration_ptr_t > concentration_container_t;

#endif // _CONCENTRATIONS_CONCENTRATION_H_
