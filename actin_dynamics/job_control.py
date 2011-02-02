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

import elixir

from .io import database

from . import utils

def job_iterator():
    job = True
    while job:
        job = get_job()
        if job:
            yield job

def get_job():
    job_query = database.Job.query.filter_by(in_progress=False, complete=False)
    job = None
    while not job:
        if not job_query.count():
            break

        try:
            job = job_query.with_locking('update_nowait').one()
            job.in_progress = True
            elixir.session.commit()
        except:
            elixir.session.rollback()
            job = None

    return job


def cleanup_jobs():
    job_query = database.Job.query

    job_query.filter_by(in_progress=True).update(in_progress=False, complete=False)
    job_query.filter_by(complete=True).delete()
    elixir.session.commit()


def create_jobs(parameter_iterator, group_name):
    group = database.Group.get_or_create(name=group_name)
    group.revision = utils.get_mercurial_revision()

    for parameters in parameter_iterator:
        database.Job.from_parameters_dict(parameters, group)

    elixir.session.commit()

def complete_job(job):
    job.complete = True
    job.in_progress = False
    elixir.session.commit()
