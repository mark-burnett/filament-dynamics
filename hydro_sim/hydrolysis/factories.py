#    Copyright (C) 2010 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import predicates
from barbed_only import BarbedOnly

def constant_random(rates, free_barbed_end, free_pointed_end):
    results = []
    if free_pointed_end:
        raise NotImplementedError('Pointed end hydrolysis.')
    elif free_barbed_end: # Barbed end only
        for state, (rate, out) in rates.items():
            results.append(BarbedOnly(predicates.Random(state), rate, out))
    return results

def constant_random_bulk(rates, free_barbed_end, free_pointed_end):
    results = []
    if free_pointed_end:
        raise NotImplementedError('Pointed end hydrolysis.')
    elif free_barbed_end: # Barbed end only
        for state, (rate, out) in rates.items():
            try:
                # Multiple rates indicate a different tip rate.
                iter(rate)
                # Bulk rate.
                results.append(BarbedOnly(
                    predicates.Random(state, 1), rate[0], out))
                # Tip rate.
                results.append(BarbedOnly(
                    predicates.SingleIndex(state, -1), rate[1], out))
                results.append(BarbedOnly(
                    predicates.SingleIndex(state, 0), rate[1], out))
            except TypeError: # rate is not iterable
                # Single rate is the same as random.
                results.append(BarbedOnly(predicates.Random(state), rate, out))
    return results

def constant_cooperative(rates, free_barbed_end, free_pointed_end):
    results = []
    if free_barbed_end:
        for state, data in rates.items():
            for neighbor, (rate, out) in data.items():
                results.append(BarbedOnly(
                        predicates.Cooperative(state, neighbor), rate, out))
    if free_pointed_end:
        raise NotImplementedError('Pointed end hydrolysis.')
    return results

_factory_dispatch = {'random':      constant_random,
                     'vectorial':   constant_cooperative,
                     'cooperative': constant_cooperative,
                     'lipowsky':    constant_cooperative,
                     'random_bulk': constant_random}

def constant_rates(model_type, rates, free_barbed_end, free_pointed_end):
    return _factory_dispatch[model_type.lower()](rates,
                                                 free_barbed_end,
                                                 free_pointed_end)
