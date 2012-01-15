#ifndef _END_CONDITIONS_DURATION_H_
#define _END_CONDITIONS_DURATION_H_
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

#include "end_conditions/end_condition.h"

#include "concentrations/concentration.h"
#include "filaments/filament.h"

class Duration : public EndCondition {
    public:
        Duration(double stop_time) : _stop_time(stop_time) {}
        void initialize(const filament_container_t &filaments,
                const concentration_container_t &concentrations) {};

        bool satisfied(double time,
                const filament_container_t &filaments,
                const concentration_container_t &concentrations) {
            return time > _stop_time;
        }
    private:
        double _stop_time;
};

#endif // _END_CONDITIONS_DURATION_H_

