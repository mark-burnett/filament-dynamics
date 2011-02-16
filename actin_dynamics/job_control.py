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

import os
import time

import elixir

#from .io import database

from . import utils


PID = os.getpid()


def job_iterator():
    job = True
    while job:
        job = get_job()
        if job:
            yield job

def get_job():
    try:
        return _get_job_mysql()
    except elixir.sqlalchemy.exc.OperationalError:
        elixir.session.rollback()
        global get_job
        get_job = _get_job_fallback
        return _get_job_fallback()

def _get_job_mysql():
    update_sql = 'UPDATE job SET pid = %s WHERE pid = 0 LIMIT 1;' % PID
    if elixir.metadata.bind.execute(update_sql):
        # There should be exactly one of these.
        return database.Job.query.filter_by(pid=PID, complete=False).first()

def _get_job_fallback():
    job_query = database.Job.query.filter_by(pid=0, complete=False)
    job = job_query.with_lockmode('update').first()
    if job:
        job.pid = PID
        elixir.session.commit()

    return job


def cleanup_jobs():
    job_query = database.Job.query

    job_query.filter_by(complete=True).delete()
    job_query.update({'pid': 0})
    elixir.session.commit()


def create_jobs(parameter_iterator, object_graph_yaml, group_name):
    group = database.Group.get_or_create(name=group_name)
    group.revision = utils.get_mercurial_revision()
    group.object_graph = object_graph_yaml

    for pars in parameter_iterator:
        job = database.Job.from_parameters_dict(pars, group)
        elixir.session.commit()


def complete_job(job):
    job.complete = True
    elixir.session.commit()


def delete_all_jobs():
    database.Job.query.delete()
    elixir.session.commit()


def duplicate_jobs_exist():
    for i1, j1 in enumerate(database.Job.query):
        j1p = j1.parameters_dict
        for i2, j2 in enumerate(database.Job.query):
            if i1 != i2 and j1p == j2.parameters_dict:
                return j1, j2

def duplicate_results_exist(group):
    for i1, r1 in enumerate(database.Run.query.filter_by(group=group)):
        for i2, r2 in enumerate(database.Run.query.filter_by(group=group)):
            if i1 != i2 and r1.job_id == r2.job_id:
                return r1, r2
