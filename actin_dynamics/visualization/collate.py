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

from actin_dynamics import database
from actin_dynamics.io import data


def collate_asymptotic_adppi(db_session, ids, filename=None,
        x_name = 'initial_pi_concentration', y_name = 'asymptotic_adppi',
        column_name='release_cooperativity', experiment_index=0):
    results = _simple_collate(db_session, ids, x_name, y_name,
            column_name, experiment_index)

    # scale results (* ftc / total f-actin)
    ftc = _get_ftc(db_session, ids, experiment_index)
    total_factin = _get_total_factin(db_session, ids, experiment_index)
#    print 'scale factor:', ftc /total_factin

    scaled_results = _scale_results(results, ftc / total_factin)

    if filename:
        _write_results(filename, scaled_results, x_name, y_name, column_name)

    return scaled_results


def basic_collate(db_session, ids, filename=None,
        x_name='filament_tip_concentration', y_name='halftime',
        column_name='release_cooperativity', experiment_index=0):
    results = _simple_collate(db_session, ids, x_name, y_name,
            column_name, experiment_index)

    if filename:
        _write_results(filename, results, x_name, y_name, column_name)

    return results


def adp_nh_collate(db_session, adp_ids, nh_ids, filename=None,
        y_name='halftime', column_name='release_cooperativity',
        experiment_index=0):
    adp_results = _simple_collate(db_session, adp_ids, 
            'fraction_adp', y_name, column_name, experiment_index)
    nh_results = _simple_collate(db_session, nh_ids,
            'fraction_nh_atp', y_name, column_name, experiment_index)

    combined_results = _combine_results(nh_results, adp_results)

    if filename:
        _write_results(filename, combined_results, 'nh (adp) fraction',
                y_name, column_name)


def _simple_collate(db_session, ids, x_name, y_name,
        column_name, experiment_index):
    accumulated_results = []
    for session in _loop_sessions(db_session, ids):
        experiment = session.experiments[experiment_index]
        accumulated_results.append((experiment.all_parameters[column_name],
            _get_xy(db_session, experiment, x_name, y_name)))
    accumulated_results.sort()

    # Do the collation..
    column_ids = [ar[0] for ar in accumulated_results]
    xs = accumulated_results[0][1][0]
#    ys = [ar[1][1] for ar in accumulated_results]
    rows = []
    for i, x in enumerate(xs):
        row = [x]
        for ar in accumulated_results:
            row.append(ar[1][1][i])
#        print 'r1:', row[1]
        rows.append(row)

    return column_ids, rows


def _combine_results(positive_results, negative_results, average_center=False):
    pos_cols, pos_rows = positive_results
    neg_cols, neg_rows = negative_results

    result = _flip_neg(neg_rows)
    if average_center:
        raise NotImplementedError()
    else:
        result.extend(pos_rows)
        return pos_cols, result



def _flip_neg(rows):
    result = []
    for row in reversed(rows):
        rrow = [-row[0]]
        rrow.extend(row[1:])
        result.append(rrow)
    return result


def _write_results(filename, results, x_name, y_name, column_name):
    column_ids, rows = results
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


def _loop_sessions(db_session, ids):
    for sid in ids:
        yield db_session.query(database.Session).filter_by(id=sid).first()


def _get_xy(db_session, experiment, x_name=None, y_name=None):
    ob = experiment.objectives[y_name]
    xy = []
    for objective in db_session.query(database.Objective).filter_by(bind=ob):
        x = objective.all_parameters[x_name]
        y = objective.value
        xy.append((x, y))

    xy.sort()
    return zip(*xy)

def _get_ftc(db_session, ids, experiment_id):
    s = db_session.query(database.Session).filter_by(id=ids[0]).first()
    e = s.experiments[experiment_id]
    r = e.runs[0]

    return r.all_parameters['filament_tip_concentration']

def _get_total_factin(db_session, ids, experiment_id):
    s = db_session.query(database.Session).filter_by(id=ids[0]).first()
    e = s.experiments[experiment_id]
    r = e.runs[0]

    pars = r.all_parameters

    total = pars.get('seed_concentration', 0)
    total += pars.get('initial_concentration', 0)

    return total

def _scale_results(results, factor):
    column_ids, rows = results

    scaled_rows = []
    for row in rows:
        if None not in row:
            scaled_row = [row[0]] + [r * factor for r in row[1:]]
            scaled_rows.append(scaled_row)

    return column_ids, scaled_rows
