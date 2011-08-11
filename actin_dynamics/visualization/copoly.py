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

import csv

from actin_dynamics.io import data
from actin_dynamics import database

def save(adp_session_ids, nh_session_ids,
        cooperativities=[1, 10, 100, 1000, 10000, 1000000],
        adp_timecourse_cooperativities=[1000],
        nh_timecourse_cooperativities=[1000],
        adp_halftime_filename='results/adp_copoly_halftimes.dat',
        nh_halftime_filename='results/nh_copoly_halftimes.dat',
        adp_timecourse_filename='results/adp_copoly_timecourses.dat',
        nh_timecourse_filename='results/nh_copoly_timecourses.dat'):
    dbs = database.DBSession()

    adp_sessions, adp_cooperativities = _get_sessions(dbs, adp_session_ids, cooperativities)
    nh_sessions, nh_cooperativities = _get_sessions(dbs, nh_session_ids, cooperativities)

    adp_halftime_results = _get_halftimes(adp_sessions)
    nh_halftime_results = _get_halftimes(nh_sessions)

#    adp_timecourse_results = _get_timecourses(adp_sessions,
#            adp_timecourse_cooperativities)
#    nh_timecourse_results = _get_timecourses(nh_sessions,
#            nh_timecourse_cooperativities)

    _write_results(adp_halftime_filename, _create_rows(adp_halftime_results),
            'ADP Fraction', 'Halftime', 'Release Cooperativity',
            adp_cooperativities)
    _write_results(nh_halftime_filename, _create_rows(nh_halftime_results),
            'NH Fraction', 'Halftime', 'Release Cooperativity',
            nh_cooperativities)



def _get_sessions(dbs, session_ids, cooperativities):
    sessions = []
    for sid in session_ids:
        s = dbs.query(database.Session).get(sid)
        if s.parameters['release_cooperativity'] in cooperativities:
            sessions.append(s)
#    sessions = [dbs.query(database.Session).get(sid) for sid in session_ids]
    sessions.sort(key=lambda s: s.parameters['release_cooperativity'])
    return sessions, [s.parameters['release_cooperativity'] for s in sessions]

def _get_halftimes(sessions):
    results = []
    for s in sessions:
        e = s.experiments[0]
        ob = e.objectives['halftime']
        session_results = []
        for o in ob.objectives:
            value = o.value
            # XXX This assumes we are only varying one parameter.
            parameter = o.run.parameters.values()[0]
            session_results.append((parameter, value))
        session_results.sort()
        parameters, values = zip(*session_results)
        results.append(values)
    return parameters, results

def _create_rows(results):
    parameters, values = results
    values.insert(0, parameters)
    return zip(*values)

def _write_results(filename, rows, x_name, y_name, column_name, column_ids):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        f.write('# columns: %s\n' % column_name)
        f.write('#     %s\n\n' % column_ids)
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(rows)
