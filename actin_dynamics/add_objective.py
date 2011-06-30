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

import database
import factories.bindings

from primitives import objectives


def add_multiple(db_session, ids, class_name=None, label=None,
        variable_arguments={}, **kwargs):
    for sid in ids:
        s = db_session.query(database.Session).filter_by(id=sid).first()
        exp = s.experiments[0]
        bind = database.ObjectiveBind(class_name=class_name, label=label,
                variable_arguments=variable_arguments, fixed_arguments=kwargs)
        bind.module_name = 'objectives'
        exp.objective_list.append(bind)

        for run in exp.runs:
            o = factories.bindings.db_single(bind, run.all_parameters)

            objective = database.Objective(run=run, bind=bind)
            o.perform(run, objective)

    db_session.commit()
