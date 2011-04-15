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

from .base_classes import Objective as _Objective
from actin_dynamics.numerical import residuals as _residuals

from actin_dynamics.numerical import regression

class DiffusionCoefficient(_Objective):
    def __init__(self, analysis_name=None, label=None):
        self.analysis_name = analysis_name

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        taus, variances, errors = run.analyses[self.analysis_name]

        # Calculate slope of line through points using residual function
        m = regression.fit_zero_line(taus, variances)

        # Calculate D (D = slope / 2) and assign the residual to target.value
        D = m / 2
        target.value = D


class DiffusionCoefficientFit(_Objective):
    def __init__(self, analysis_name=None, expected_value=None, label=None,
                 residual_type=None):
        self.analysis_name     = analysis_name
        self.expected_value    = expected_value
        self.residual_function = getattr(_residuals, residual_type)

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        taus, variances, errors = run.analyses[self.analysis_name]

        # Calculate slope of line through points using residual function
        m = regression.fit_zero_line(taus, variances)

        # Calculate D (D = slope / 2) and assign the residual to target.value
        D = m / 2
        target.value = self.residual_function([None, [D]],
                                              [None, [self.expected_value]])
