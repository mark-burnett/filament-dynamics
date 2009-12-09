#    Copyright (C) 2009 Mark Burnett
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

def simulate(strand, steps, rates, data_collectors, rng):
    # Initialize data storage dictionary
    data = dict( (key, []) for key in data_collectors.keys() )

    # Use local names to get rid of a bunch of useless lookups
    poly        = rates.poly
    depoly      = rates.depoly
    trans       = rates.transition
    trans_b     = rates.transition_barbed
    trans_p     = rates.transition_pointed
    poly_state  = rates.poly_state
    window_size = rates.window_size

    if window_size % 2:
        shift = (window_size - 1) / 2
    else:
        shift = window_size / 2

    for step in xrange(steps):
        # Polymerize
        if rng() < poly():
            strand.append(poly_state)
        # Depolymerize
        if rng() < depoly(strand[-1]):
            try:
                strand.pop()
            except IndexError:
                # NOTE: This will not let the data collectors collect this step.
                break

        # FIXME This is technically questionable, as hydrolysis will slightly
        #       depend on the ordering of the hydrolysis. I should consider
        #       copying every time, though it would be slower.

        # Hydrolize pointed end
        for i in xrange(shift):
            probs = trans_p(strand[max(0, i-shift):i-shift+window_size])
            strand[i] = _choose_state(probs, rng(), strand[i])
        # Hydrolize the builk of the filament
        for i in xrange(len(strand) - window_size):
            probs = trans(strand[i:i + window_size])
            if probs:
                strand[i + shift] = _choose_state(probs, rng(), strand[i])
        # Hydrolize barbed end
        for i in xrange(window_size - shift - 1):
            raise RuntimeError('Barbed end special case not written.')

        # Collect and store data
        for key, f in data_collectors.items():
            result = f(**locals())
            if result is not None:
                data[key].append(result)

    return data

def _choose_state(probs, num, default=None):
    """
    Selects a state from probs given an already generated random number, num.
    """
    for rate, state in probs:
        if num < rate:
            return state

    return default
