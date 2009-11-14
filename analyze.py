#!/usr/bin/env python
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

import sys
import cPickle
import itertools
from multiprocessing import Pool, Process

from numpy import array, average

from states import ChemicalState
import diffusion

# Analysis parameters
input_file_name = 'analyze_in.pickle'
trash_time = 2500

# Ideally placeholder_tuple would be *args, but that is difficult to do with
# izip/itertools (as far as I can tell).
def analyze(placeholder_tuple):
    c, output, dt = placeholder_tuple
    trash_samples = int(trash_time/dt)
    length = output['length'   ][ trash_samples: ]
    cl     = output['cap_len'  ][ trash_samples: ]
    ac     = output['ATP_cap'  ][ trash_samples: ]
    ts     = output['tip_state'][ trash_samples: ]
    tT  = float(sum(itertools.imap(lambda x: ChemicalState.ATP == x, ts))
               )/len(ts)
    tDp = float(sum(itertools.imap(lambda x: ChemicalState.ADPPi == x, ts))
               )/len(ts)
    tD  = float(sum(itertools.imap(lambda x: ChemicalState.ADP == x, ts))
               )/len(ts)

    # All our crazy v and d calculations
    window_size = int(2000 / dt)
    given_v = -0.873

    V  = diffusion.fit_velocity(length, dt)
    Vd = diffusion.window_velocity(length, window_size, dt)

    D  = diffusion.naive_diffusion(length, window_size, dt)
    Dg = diffusion.given_v_diffusion(length, given_v, window_size, dt)
    Ds = diffusion.subtracted_v_diffusion(length, given_v, window_size, dt)

    cap_len = average(cl)
    atp_len = average(ac)
    map(lambda x: sys.stdout.write('%5.3f ' % x),
            [c, tT, tDp, tD, tT+tDp+tD, cap_len, atp_len, V, Vd, D, Dg, Ds])
    print
    return V, Vd, D, Dg, Ds

def go():
    results = cPickle.load(file(input_file_name))
    p = Pool()
    print 'c'.ljust(5), 'tT'.ljust(5), 'tDp'.ljust(5), 'tD'.ljust(5), 'total',\
          'cap'.ljust(5), 'atp_c'.ljust(5),\
          'V'.ljust(5), 'Vd'.ljust(5), 'D'.ljust(5), 'Dg'.ljust(5),\
          'Ds'.ljust(5)
    outputs = p.map(analyze,
                    itertools.izip(results['concentrations'], results['data'],
                                   itertools.repeat(results['dt'])))
    p.close()
    p.join()

if '__main__' == __name__:
    p = Process(target = go)
    p.start()
    p.join()
