#ifndef _CONCENTRATIONS_FIXED_REAGENT_H_
#define _CONCENTRATIONS_FIXED_REAGENT_H_
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

#include "concentration.h"

namespace stochastic {
namespace concentrations {

class FixedReagent : public Concentration {
    public:
        FixedReagent(double concentration, double fnc, size_t number_of_filaments=1) :
            _number(concentration * number_of_filaments /fnc),
            _volume(number_of_filaments / fnc) {}
        ~FixedReagent() {}

        double value() const { return _number / _volume; }
        void add_monomer() { ++_number;};
        void remove_monomer() { if (_number > 0) --_number;};
        size_t monomer_count() { return _number; }
    private:
        size_t _number;
        double _volume;
};


} // namespace concentrations
} // namespace stochastic

#endif // _CONCENTRATIONS_FIXED_REAGENT_H_
