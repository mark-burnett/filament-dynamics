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

from .base_classes import Analyst

from actin_dynamics import database

class SaveObservation(Analyst):
    def __init__(self, observation_name=None, *args, **kwargs):
        self.observation_name = observation_name
        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        # NOTE run_support needs to attach run & binding to this result
        return database.Analysis(value=observations[self.observation_name])
