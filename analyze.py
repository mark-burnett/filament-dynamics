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
from itertools import izip
from multiprocessing import Pool, Process

from numpy import array, average

from states import ChemicalState
import diffusion

# Analysis parameters
input_file_name = '0_1_160000s_8runs.pickle'
trash_time = 2500

def analyze(i, c, results):
    strand, output = results
    sample_period = output['sample_period']
    trash_samples = int(trash_time/sample_period)
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
    V, v_const  = diffusion.fit_velocity(length, sample_period)
    tip_v = c * 11.6 - tT * 1.4 - tDp * 1.1 - tD * 7.2
    end_v = (length[-1]-length[0])/(sample_length*len(length))
    print i, V, tip_v, end_v

#    with file(str(i)+'win.dat', 'w') as outfile:
#        for t_window_size in [10,25,50,75,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2250,2500,2750,3000]:
#            window_size = int(t_window_size/dt)
#
#            D    = diffusion.naive_diffusion(length, window_size, dt)
#
#            DgV  = diffusion.given_v_diffusion(length, V, window_size, dt)
#            DsV  = diffusion.subtracted_v_diffusion(length, V, window_size, dt)
#
#            DgtV = diffusion.given_v_diffusion(length, tip_v, window_size, dt)
#            DstV = diffusion.subtracted_v_diffusion(length, tip_v, window_size,
#                                                    dt)
#
#            DgeV = diffusion.given_v_diffusion(length, end_v, window_size, dt)
#            DseV = diffusion.subtracted_v_diffusion(length, end_v, window_size,
#                                                    dt)
#            outfile.write('%s %s %s %s %s %s %s %s\n' %
#                          (t_window_size, D, DgV, DsV, DgtV, DstV, DgeV, DseV))
#
    cap_len = average(cl)
    atp_len = average(ac)
    map(lambda x: sys.stdout.write('%5.3f ' % x),
            [c, tT, tDp, tD, tT+tDp+tD, cap_len, atp_len,
             V, Vd, tip_v, D, Dg, Ds])
    print
    return V, Vd, tip_v, D, Dg, Ds

if '__main__' == __name__:
    with file(input_file_name) as f:
        results = cPickle.load(f)
    p = Pool()
    concentrations = results['concentrations']
    data = results['data']
    dt = results['dt']
    try:
        for (i,c), d in izip(enumerate(concentrations),data):
            p.apply_async(analyze, (i, c, d))
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
#    f = file('d_c.dat','w')
#    for c, (V, Vd, tip_v, D, Dg, Ds) in zip(results['concentrations'],
#                                              outputs):
#        f.write('%s %s %s %s %s %s %s\n' % (c, V, Vd, tip_v, D, Dg, Ds))
#    f.close()
