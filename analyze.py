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
input_file_name = '0_1_160000s_8runs.pickle'
trash_time = 2500

# Ideally placeholder_tuple would be *args, but that is difficult to do with
# izip/itertools (as far as I can tell).
#def analyze(placeholder_tuple):
def analyze(i, c, results, dt):
    strand, output = results
#    c, (final_strand, output), dt = placeholder_tuple
#    c, output, dt = placeholder_tuple
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
    V, v_const  = diffusion.fit_velocity(length, dt)
    tip_v = c * 11.6 - tT * 1.4 - tDp * 1.1 - tD * 7.2
    end_v = (length[-1]-length[0])/(dt*len(length))
    print i, V, tip_v, end_v
#    print c, tT, tDp, tD, V, tip_v
#    print diffusion.tip_state_velocities(length, ts, dt)
#    print (length[-1]-length[0])/(dt*len(length))
    outfile = file(str(i)+'win.dat', 'w')
    for t_window_size in [10,25,50,75,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2250,2500,2750,3000]:
        window_size = int(t_window_size/dt)

        D    = diffusion.naive_diffusion(length, window_size, dt)

        DgV  = diffusion.given_v_diffusion(length, V, window_size, dt)
        DsV  = diffusion.subtracted_v_diffusion(length, V, window_size, dt)

        DgtV = diffusion.given_v_diffusion(length, tip_v, window_size, dt)
        DstV = diffusion.subtracted_v_diffusion(length, tip_v, window_size, dt)

        DgeV = diffusion.given_v_diffusion(length, end_v, window_size, dt)
        DseV = diffusion.subtracted_v_diffusion(length, end_v, window_size, dt)

#        outfile.write('%s %s\n' % (t_window_size, D))
        outfile.write('%s %s %s %s %s %s %s %s\n' %
                      (t_window_size, D, DgV, DsV, DgtV, DstV, DgeV, DseV))
    outfile.close()

#    cap_len = average(cl)
#    atp_len = average(ac)
#    map(lambda x: sys.stdout.write('%5.3f ' % x),
#            [c, tT, tDp, tD, tT+tDp+tD, cap_len, atp_len,
#             V, Vd, tip_v, D, Dg, Ds])
#    print
#    return V, Vd, tip_v, D, Dg, Ds

if '__main__' == __name__:
    results = cPickle.load(file(input_file_name))
    p = Pool(1)
    concentrations = results['concentrations']
    data = results['data']
    dt = results['dt']
    try:
        for (i,c), d in itertools.izip(enumerate(concentrations),data):
            p.apply_async(analyze, (i, c, d, dt))
#        outputs = p.map(analyze,
#                        itertools.izip(results['concentrations'],
#                                       results['data'],
#                                       itertools.repeat(results['dt'])))
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
#    f = file('d_c.dat','w')
#    for c, (V, Vd, tip_v, D, Dg, Ds) in zip(results['concentrations'],
#                                              outputs):
#        f.write('%s %s %s %s %s %s %s\n' % (c, V, Vd, tip_v, D, Dg, Ds))
#    f.close()
