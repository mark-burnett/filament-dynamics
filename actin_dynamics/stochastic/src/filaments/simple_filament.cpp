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

#include "filaments/simple_filament.h"

SimpleFilament::SimpleFilament(_vector_ui_ci start, _vector_ui_ci stop) {
    while (start < stop) {
        filamentss.push_back(*start);
        ++start;
    }
}

SimpleFilament::SimpleFilament(size_t number, size_t filaments) {
    for (size_t i = 0; i < number; ++i) {
        filamentss.push_back(filaments);
    }
}

// Simple queries about the filament filaments.
size_t SimpleFilament::filaments_count(size_t filaments) const {
    size_t count = 0;
    for (std::deque<size_t>::const_iterator i = filamentss.begin();
            i < filamentss.end(); ++i) {
        if (*i == filaments) {
            ++count;
        }
    }

    return count;
}

size_t SimpleFilament::boundary_count(size_t pointed_filaments,
        size_t barbed_filaments) const {
    size_t count = 0;

    std::deque<size_t>::const_iterator pointed = filamentss.begin();
    std::deque<size_t>::const_iterator barbed = filamentss.begin();
    ++barbed;
    while (barbed < filamentss.end()) {
        if (*pointed == pointed_filaments && *barbed == barbed_filaments) {
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }

    return count;
}

size_t SimpleFilament::length() const {
    return filamentss.size();
}

size_t SimpleFilament::barbed_filaments() const {
    return filamentss.back();
}

size_t SimpleFilament::pointed_filaments() const {
    return filamentss.front();
}


// Add and remove subunits
void SimpleFilament::append_barbed(size_t new_filaments) {
    filamentss.push_back(new_filaments);
}

void SimpleFilament::append_pointed(size_t new_filaments) {
    filamentss.push_front(new_filaments);
}

size_t SimpleFilament::pop_barbed() {
    size_t filaments = filamentss.back();
    filamentss.pop_back();
    return filaments;
}

size_t SimpleFilament::pop_pointed() {
    size_t filaments = filamentss.front();
    filamentss.pop_front();
    return filaments;
}


// Update filamentss
void SimpleFilament::update_filaments(size_t instance_number,
        size_t old_filaments, size_t new_filaments) {
    size_t count = 0;
    for (std::deque<size_t>::iterator i = filamentss.begin();
            i < filamentss.end(); ++i) {
        if (*i == old_filaments) {
            if (count == instance_number) {
                *i = new_filaments;
                return;
            }
            ++count;
        }
    }
}

void SimpleFilament::update_boundary(size_t instance_number,
        size_t old_pointed_filaments, size_t old_barbed_filaments,
        size_t new_pointed_filaments, size_t new_barbed_filaments) {
    size_t count = 0;

    std::deque<size_t>::iterator pointed = filamentss.begin();
    std::deque<size_t>::iterator barbed = filamentss.begin();
    ++barbed;
    while (barbed < filamentss.end()) {
        if (*pointed == old_pointed_filaments && *barbed == old_barbed_filaments) {
            if (count == instance_number) {
                *pointed = new_pointed_filaments;
                *barbed = new_barbed_filaments;
            }
            ++count;
            ++pointed;
            ++barbed;
        }
        ++pointed;
        ++barbed;
    }
}
