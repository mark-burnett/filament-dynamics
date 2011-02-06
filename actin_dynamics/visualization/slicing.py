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

from actin_dynamics.io import database

# 2d slicing:
#   straight slices
#   reductions
#
#   ordinate options: analysis value, run value
#   abscissa options: analysis parameter, run parameter

import elixir

def rv_rp_reduce(group, value_name=None, parameter_name=None,
                 reduction_function=min):
    group_runs = database.Run.query.filter_by(group=group)
    abscissa_values = _get_parameters_mesh(group_runs, parameter_name)
    ordinate_values = []

    base_run_id_query = database.SimulationParameter.query.filter(
            database.SimulationParameter.run_id.in_(r.id for r in group_runs)
            ).filter_by(name=parameter_name)
    for x in abscissa_values:
        # Get run ids that match this abscissa
        run_id_query = base_run_id_query.filter_by(value=x)

        # Get values that match run_ids
        values_query = database.SimulationValue.query.filter_by(
                name=value_name).filter(
                        database.SimulationValue.run_id.in_(
                            sp.run_id for sp in run_id_query))
        value = reduction_function(v.value for v in values_query)
        ordinate_values.append(value)

    return abscissa_values, ordinate_values


def av_ap_reduce(group, value_name=None, parameter_name=None,
                 reduction_function=min):
    run = database.Run.query.filter_by(group=group).first()
    abscissa_values = _get_parameters_mesh(
            database.Analysis.query.filter_by(run=run), parameter_name)

    ordinate_values = []

    group_runs = database.Run.query.filter_by(group=group)
    group_analysis = database.Analysis.query.filter(
            database.Analysis.run_id.in_(r.id for r in group_runs))
    base_analysis_parameter_query = (database.AnalysisParameter.query
            .filter_by(name=parameter_name)
            .filter(database.AnalysisParameter.analysis_id.in_(
                a.id for a in group_analysis)))
    for x in abscissa_values:
        # Get run ids that match this abscissa
        analysis_parameter_query = base_analysis_parameter_query.filter_by(
                value=x)

        # Get values that match run_ids
        values_query = (database.AnalysisValue.query
                .filter_by(name=value_name)
                .filter(database.AnalysisValue.analysis_id.in_(
                    ap.analysis_id for ap in analysis_parameter_query)))
        value = reduction_function(v.value for v in values_query)
        ordinate_values.append(value)

    return abscissa_values, ordinate_values


def _get_parameters_mesh(iterator, parameter_name):
    values = set()
    for i in iterator:
        values.add(i.get_parameter(parameter_name))
    return sorted(values)

# 3d slicing:
#   straight slices
#   reductions
#
#   ordinate options: analysis value, run value
#   abscissae options: [(ap | rp), (ap | rp)]
