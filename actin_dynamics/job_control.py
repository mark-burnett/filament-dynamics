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

import time

import elixir

from .io import database

from . import utils

def job_iterator():
    job = True
    while job:
        job = get_job()
        if job:
            yield job

def get_job(retries=1000, sleep_time=0.005):
    job_query = database.Job.query.filter_by(in_progress=False, complete=False)
    for i in xrange(retries):
        try:
            job = job_query.with_lockmode('update_nowait').first()
            if job is None:
                return
            job.in_progress = True
            elixir.session.commit()
            return job
        except elixir.sqlalchemy.exceptions.OperationalError:
            elixir.session.rollback()
            time.sleep(sleep_time)
            if not job_query.count():
                return
    raise RuntimeError('Failed to get a job.  Giving up after %s retries.' % retries)


def cleanup_jobs():
    job_query = database.Job.query

    job_query.filter_by(complete=True).delete()
#    for job in job_query.filter_by(complete=True):
#        job.delete()
    job_query.filter_by(in_progress=True).update({'in_progress': False,
                                                  'complete': False})
    elixir.session.commit()


def create_jobs(parameter_iterator, object_graph_yaml, group_name, flush_count=100):
    group = database.Group.get_or_create(name=group_name)
    group.revision = utils.get_mercurial_revision()
    group.object_graph = object_graph_yaml

    i = 0
    for pars in parameter_iterator:
        job = database.Job.from_parameters_dict(pars, group)
        i += 1
        if flush_count == i:
            elixir.session.flush()
            i = 0

    elixir.session.commit()

def complete_job(job):
    job.complete = True
    job.in_progress = False
    elixir.session.commit()

def delete_all_jobs():
    database.Job.query.delete()
    elixir.session.commit()
