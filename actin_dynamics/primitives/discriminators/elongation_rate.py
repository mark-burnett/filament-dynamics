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

from actin_dynamics.numerical import measurements

class ElongationRate(_Objective):
    def __init__(self, sample_period=None, label=None):
        self.sample_period = sample_period

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        length = run.analyses['length']
        target.value = measurements.derivative(length)[-1]

class SquaredElongationRate(_Objective):
    def __init__(self, sample_period=None, label=None):
        self.sample_period = sample_period

        _Objective.__init__(self, label=label)

    def perform(self, run, target):
        length = run.analyses['length']
        target.value = measurements.derivative(length)[-1]**2
