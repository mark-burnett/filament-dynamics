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
#input_file_name = '0_01_to_0_1.pickle'
#input_file_name = '0_1.pickle'
input_file_name = '0_1_10,000s.pickle'
trash_time = 5000

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
    given_v = tT * c * 11.6 - tT * 1.4 - tDp * 1.1 - tD * 7.2
    V, v_const  = diffusion.fit_velocity(length, dt)
    Dlol = diffusion.naive_subtracted(length, V, v_const, dt)
    print c, tT, tDp, tD, V, given_v, Dlol
#    window_size = int(2000 / dt)
#    given_v = -0.873
    outfile = file('d_ws.dat', 'w')
    for t_window_size in [10,25,50,75,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2250,2500,2750,3000]:
        window_size = int(t_window_size/dt)
#        Vd = diffusion.window_velocity(length, window_size, dt)

        D  = diffusion.naive_diffusion(length, window_size, dt)
#        Dg = diffusion.given_v_diffusion(length, given_v, window_size, dt)
#        Ds = diffusion.subtracted_v_diffusion(length, given_v, window_size, dt)
        outfile.write('%s %s\n'%# %s %s %s\n' %
                      (t_window_size, D)) #, Dg, Ds))
    outfile.close()

    cap_len = average(cl)
    atp_len = average(ac)
#    map(lambda x: sys.stdout.write('%5.3f ' % x),
#            [c, tT, tDp, tD, tT+tDp+tD, cap_len, atp_len,
#             V, Vd, given_v, D, Dg, Ds])
#    print
#    return V, Vd, given_v, D, Dg, Ds

#def go():
if '__main__' == __name__:
    results = cPickle.load(file(input_file_name))
    p = Pool()
#    print 'c'.ljust(5), 'tT'.ljust(5), 'tDp'.ljust(5), 'tD'.ljust(5), 'total',\
#          'cap'.ljust(5), 'atp_c'.ljust(5),\
#          'V'.ljust(5), 'Vd'.ljust(5), 'Vg'.ljust(5),\
#          'D'.ljust(5), 'Dg'.ljust(5), 'Ds'.ljust(5)
    try:
        outputs = p.map(analyze,
                        itertools.izip(results['concentrations'], results['data'],
                                       itertools.repeat(results['dt'])))
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
#    f = file('d_c.dat','w')
#    for c, (V, Vd, given_v, D, Dg, Ds) in zip(results['concentrations'],
#                                              outputs):
#        f.write('%s %s %s %s %s %s %s\n' % (c, V, Vd, given_v, D, Dg, Ds))
#    f.close()
