#    Copyright (C) 2010 Mark Burnett
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

import itertools
import elixir

from . import accessors as _accessors
from . import fluorescence as _fluorescence
from . import interpolation as _interpolation
from . import residuals as _residuals

from actin_dynamics import io

def pyrene_analysis(group, atp_weights=[0.37],
                    adppi_weights=[0.56],
                    adp_weights=[0.75]):
    run = io.database.Run.query.filter_by(group=group).first()
    sample_times = run.get_measurement('pyrene_atp_count')[0]
    pyrene_data = io.pollard.get_interpolated_pyrene_data(sample_times)
    for run in group.runs:
        for (atp_weight, adppi_weight, adp_weight
                ) in itertools.product(atp_weights, adppi_weights, adp_weights):
            fit, norm = _fluorescence.get_pyrene_fit(run,
                                                     pyrene_data=pyrene_data,
                                                     atp_weight=atp_weight,
                                                     adppi_weight=adppi_weight,
                                                     adp_weight=adp_weight)

            run.analyses.append(io.database.Analysis.from_dicts(
                parameter_dict={'atp_weight':   atp_weight,
                                'adppi_weight': adppi_weight,
                                'adp_weight':   adp_weight},
                value_dict={'pollard_pyrene_normalization': norm,
                            'pollard_pyrene_chi_squared':   fit}))

        elixir.session.flush()
    elixir.session.commit()


def adppi_analysis(group, flush_count=1000):
    adppi_data = io.pollard.get_adppi_data()
    i = 0
    for run in group.runs:
        fit = adppi_fit(run, adppi_data)
        run.values.extend(io.database.SimulationValue.from_dict(
            {'pollard_adppi_chi_squared': fit}))

        i += 1
        if i == flush_count:
            elixir.session.flush()
            i = 0

    elixir.session.commit()

def adppi_fit(run, data):
    # XXX We are only using pyrene adppi, we should be using both.
    simulation_data = _accessors.get_scaled(run, 'pyrene_adppi_count')

    sample_times = data[0]
    sampled_sim_data = _interpolation.resample_measurement(
            simulation_data, sample_times)

    return _residuals.naked_chi_squared(sampled_sim_data, data)
