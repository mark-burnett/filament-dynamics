#    Copyright (C) 2011 Mark Burnett
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

import pprint
import pylab

import numpy

from . import slicing
from . import measurements

from actin_dynamics import database


def both(db_session, id=1):
    print 'Tau:'
    ftc(db_session, id)
    print 'Halftime:'
    ht(db_session, id)

def ht(db_session, id=1, x_name='filament_tip_concentration'):
    s = db_session.query(database.Session).filter_by(id=id).first()
    x, y = _get_ht(db_session, s, x_name)
    x = list(1000 * numpy.array(x))
    y = list(y)
    pprint.pprint(zip(x, y))

def _get_ht(db_session, session, x_name):
    e = session.experiments[0]
    ob = e.objectives['halftime']
    result = []
    for o in db_session.query(database.Objective).filter_by(bind=ob):
        x = o.all_parameters[x_name]
        result.append((x, o.value))
    return zip(*result)


def ftc(db_session, id=1):
    s = db_session.query(database.Session).filter_by(id=id).first()
    x, y = _get_taus(s)
    x = list(1000 * numpy.array(x))
    y = list(y)
    pprint.pprint(zip(x, y))

def ftc2(session):
    runs = session.experiments[0].runs

    blah = [(r.all_parameters['filament_tip_concentration'],
        r.objectives[0].value) for r in runs]

    pprint.pprint(blah)


def go(db_session):
    sm2, sm1 = db_session.query(database.Session).all()[-2:]

    if 'ADP' in sm1.name:
        adp_session = sm1
        nh_session = sm2
    else:
        adp_session = sm2
        nh_session = sm1

    adp_meas = _get_taus(adp_session)
    nh_meas = _get_taus(nh_session)

    x = [-ax * 100 for ax in adp_meas[0][-1::-1]]
    y = [ay for ay in adp_meas[1][-1::-1]]

    x.extend([ax * 100 for ax in nh_meas[0]])
    y.extend(nh_meas[1])

    pprint.pprint(zip(x, y))


def _get_taus(session):
    e = session.experiments[0]
    s = slicing.Slicer.from_objective_bind(e.objectives['tau'])

    y, names, meshes = s.slice()

    return meshes[0], y


def pi(session):
    e = session.experiments[0]
    s = slicing.Slicer.from_objective_bind(e.objectives['tau'])

#    pylab.figure()

    y, names, meshes = s.slice()
    pprint.pprint(zip(meshes[0], y))

#    measurements.line((meshes[0], y))

def timecourse(run):
    tau = run.objectives[0].value
    magnitude = run.objectives[1].value
    ftc = run.all_parameters['filament_tip_concentration']
    print 'Tau =', tau
    print 'Magnitude =', magnitude
    print 'FTC =', ftc
    pi = run.analyses['Pi']

#    pylab.figure()
    measurements.line(pi, label='Simulated [Pi]', color='red')
    x = numpy.array(pi[0])
    y = magnitude * (1 - numpy.exp(-x / tau))
    measurements.line((x,y), label='Tau = %s' % tau, color='blue')

#    a = pylab.gca()
#    a.set_xscale('log')
#    a.set_yscale('log')

    rho = run.all_parameters['release_cooperativity']
    rate = run.all_parameters['release_rate']
#    nh_conc = run.all_parameters['initial_nh_atp_concentration']
    pylab.legend(loc=2)
    pylab.title('Copolymerization, rho = %s, rate = %s' % (rho, rate))
    pylab.xlabel('Time (seconds)')
    pylab.ylabel('Tau (seconds)')
