#ifndef _END_CONDITIONS_END_CONDITION_H_
#define _END_CONDITIONS_END_CONDITION_H_
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

#include "concentrations/concentration.h"
#include "filaments/filament.h"

namespace stochastic {
namespace end_conditions {

class EndCondition : public boost::noncopyable {
    public:
        virtual ~EndCondition() {}

        virtual void initialize(const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) = 0;

        virtual bool satisfied(double time,
                const filaments::container_t &filaments,
                const concentrations::container_t &concentrations) = 0;
    typedef boost::shared_ptr<EndCondition> ptr_t;
};

typedef std::vector< EndCondition::ptr_t > container_t;

} // namespace end_conditions
} // namespace stochastic

#endif // _END_CONDITIONS_END_CONDITION_H_
