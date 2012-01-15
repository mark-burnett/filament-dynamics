#ifndef _END_CONDITIONS_EVENT_COUNT_H_
#define _END_CONDITIONS_EVENT_COUNT_H_
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

class EventCount : public EndCondition {
    public:
        EventCount(size_t max_events) : _max_events(max_events),
            _event_count(0) {}
        void initialize(const filament_container_t &filaments,
                const concentration_container_t &concentrations) {
            _event_count = 0;
        };

        bool satisfied(double time,
                const filament_container_t &filaments,
                const concentration_container_t &concentrations) {
            ++_event_count;
            return _event_count > _max_events;
        }
    private:
        const size_t _max_events;
        size_t _event_count;
};

#endif // _END_CONDITIONS_EVENT_COUNT_H_


