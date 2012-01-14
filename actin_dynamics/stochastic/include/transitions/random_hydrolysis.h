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
#include "filaments/filament.h"

#include "transitions/transition.h"


class RandomHydrolysis : public Transition {
    public:
        RandomHydrolysis(State _old_filaments, State _new_filaments,
                double _rate) : old_filaments(_old_filaments), new_filaments(_new_filaments),
                                rate(_rate), count(0) {}
        double R(double time,
                    const boost::ptr_vector<Filament> &filaments,
                    const boost::ptr_vector<Concentration> &concentrations);
        size_t perform(double time, double r,
                    boost::ptr_vector<Filament> &filaments,
                    boost::ptr_vector<Concentration> &concentrations);
    private:
        State old_filaments;
        State new_filaments;
        double rate;

        size_t count;

        // cache
        double previous_R;
        std::vector<double> filament_Rs;
};

#endif // _TRANSITIONS_RANDOM_HYDROLYSIS_H_
