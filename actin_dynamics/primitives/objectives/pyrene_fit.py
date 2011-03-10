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
from actin_dynamics.numerical import measurements as _measurements

class PyreneFit(_Objective):
    def __init__(self, label=None, residual_type=None, **weights):
        self.residual_function = getattr(_residuals, residual_type)
        self.weights = dict((k, float(v)) for k, v in weights.iteritems())

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        data = run.experiment.objectives[self.label].measurement
        fit, measurement = self.fit_measurement(run, data)

        target.value = fit

    def unnormalized_measurement(self, run):
        analyses = run.analyses
        measurements = []
        for name, weight in self.weights.iteritems():
            measurements.append(_measurements.scale(analyses[name], weight))
        return _measurements.add(measurements)

    def fit_measurement(self, run, data):
        unnormalized_measurement = self.unnormalized_measurement(run)

        fit, norm = _pyrene_normalization(unnormalized_measurement, data,
                                          self.residual_function)
        measurement = _measurements.scale(unnormalized_measurement, norm)

        return fit, measurement


def _pyrene_normalization(fluorescence_sim=None, fluorescence_data=None,
                          residual_function=_residuals.naked_chi_squared):
    '''
    Returns chi squared of fit and normalization parameter.
    '''
    from scipy import optimize as _optimize

    # Create residual function
    def model_function(normalization):
        scaled_sim = _measurements.scale(fluorescence_sim, normalization[0])

        return residual_function(fluorescence_data, scaled_sim)

    # Use scipy to generate the results.
    normalization_guess = (float(fluorescence_data[1][-1]) /
                           fluorescence_sim[1][-1])

    fit_results = _optimize.fmin(model_function, normalization_guess,
                                 disp=False, full_output=True)

    return fit_results[1], fit_results[0][0]
