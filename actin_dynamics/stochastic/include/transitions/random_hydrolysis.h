#ifndef _TRANSITIONS_RANDOM_HYDROLYSIS_H_
#define _TRANSITIONS_RANDOM_HYDROLYSIS_H_
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

#include "concentrations/concentration.h"
#include "state/filament.h"

#include "transitions/transition.h"


class RandomHydrolysis : public Transition {
    public:
        RandomHydrolysis(unsigned int _old_state, unsigned int _new_state,
                double _rate) : old_state(_old_state), new_state(_new_state),
                                rate(_rate), count(0) {}
        double R(double time,
                    const boost::ptr_vector<Filament> &filaments,
                    const boost::ptr_vector<Concentration> &concentrations);
        size_t perform(double time, double r,
                    boost::ptr_vector<Filament> &filaments,
                    boost::ptr_vector<Concentration> &concentrations);
    private:
        unsigned int old_state;
        unsigned int new_state;
        double rate;

        size_t count;

        // cache
        double previous_R;
        std::vector<double> filament_Rs;
};

#endif // _TRANSITIONS_RANDOM_HYDROLYSIS_H_
