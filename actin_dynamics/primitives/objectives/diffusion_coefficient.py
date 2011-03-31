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

from actin_dynamics import logger
log = logger.getLogger(__file__)

class DiffusionCoefficient(_Objective):
    def __init__(self, analysis_prefix=None, label=None):
        self.analysis_prefix   = analysis_prefix

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        # Get histograms
        histograms = get_histograms(run, self.analysis_prefix)

        # Fit gaussians
        taus, means, variances = gaussian_fits(histograms)
#        log.warn('taus = %s', taus)
#        log.warn('means = %s', means)
#        log.warn('variances = %s', variances)

        # Calculate slope of line through points using residual function
        m, b = regression.fit_line(taus, variances)
#        m = regression.fit_zero_line(taus, variances)

        # Calculate D (D = slope / 2) and assign the residual to target.value
        D = m / 2
#        log.warn('slope = %s, D = %s', m, D)
#        log.warn('slope = %s, intercept = %s, D = %s', m, b, D)
        target.value = D


class DiffusionCoefficientFit(_Objective):
    def __init__(self, analysis_prefix=None, expected_value=None, label=None,
                 residual_type=None):
        self.analysis_prefix   = analysis_prefix
        self.expected_value    = expected_value
        self.residual_function = getattr(_residuals, residual_type)

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        # Get histograms
        histograms = get_histograms(run, self.analysis_prefix)

        # Fit gaussians
        taus, means, variances = gaussian_fits(histograms)

        # Calculate slope of line through points using residual function
        m, b = regression.fit_line(taus, variances)

        # Calculate D (D = slope / 2) and assign the residual to target.value
        D = m / 2
        target.value = self.residual_function([None, [D]],
                                              [None, [self.expected_value]])

def get_histograms(run, prefix):
    prefix_length = len(prefix)
    unsorted = []
    for label, analysis in run.analyses.iteritems():
        if label[:prefix_length] == prefix:
            tau = float(label[prefix_length:])
            unsorted.append((tau, analysis))

    return sorted(unsorted, key=lambda x: x[0])


def gaussian_fits(histograms):
    taus      = []
    means     = []
    variances = []
    for tau, histogram in histograms:
        taus.append(tau)

        mean, variance= regression.fit_gaussian(histogram[0], histogram[1])
        means.append(mean)
        variances.append(variance)

    return taus, means, variances
