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

from actin_dynamics import database

def calculate(session_id, parameter_name='release_rate',
        objective_name='halftime'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    runs = session.experiments[0].runs

    us_parameters = [r.parameters[parameter_name] for r in runs]
    us_objectives = [r.get_objective(objective_name) for r in runs]

    parameters, objectives = zip(*sorted(zip(us_parameters, us_objectives)))

    base_par = parameters[1]
    base_obj = objectives[1]

    low_par = (parameters[0] - base_par)
    high_par = (parameters[2] - base_par)

    low_obj = (objectives[0] - base_obj)
    high_obj = (objectives[2] - base_obj)

    low_sense = low_obj / low_par
    high_sense = high_obj / high_par

    return low_sense, high_sense
