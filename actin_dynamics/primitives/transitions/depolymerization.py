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

from base_classes import FilamentTransition as _FilamentTransition

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class _FixedRate(_FilamentTransition):
    skip_registration = True
    __slots__ = ['state', 'rate', 'check_index', 'disable_time',
            'concentration_name', 'concentration_threshold']
    def __init__(self, check_index=None, state=None, rate=None,
            concentration_name=None, concentration_threshold=None,
            disable_time=999999999, label=None):
        """
        state - state to depolymerize
        rate  - depolymerization rate (constant)
        """
        self.state       = state
        self.rate        = rate
        self.check_index = check_index
        self.disable_time = float(disable_time)

        self.concentration_name = concentration_name
        self.concentration_threshold = float(concentration_threshold)

        _FilamentTransition.__init__(self, label=label)

    def R(self, time, filaments, concentrations):
        go_ahead = time < self.disable_time
        if self.concentration_name:
            if (self.concentration_threshold <
                    concentrations[self.concentration_name].value):
                go_ahead = False

        if go_ahead:
            result = []
            for filament in filaments:
                if filament.states and self.state == filament[self.check_index]:
                    result.append(self.rate)
                else:
                    result.append(0)
            return result
        else:
            return [0 for f in filaments]

    def perform(self, time, filaments, concentrations, index, r):
        if not len(filaments[index]):
            _log.warn('Filament (index = %s) completely depolymerized.', index)
        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)

class BarbedDepolymerization(_FixedRate):
    __slots__ = []
    def __init__(self, **kwargs):
        _FixedRate.__init__(self, check_index=-1, **kwargs)

    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]
        if not current_filament.states:
            _log.error('Attempted to depolymerize empty filament.')
        current_filament.shrink_barbed_end()
        concentrations[self.state].add_monomer(time)
        _FixedRate.perform(self, time, filaments, concentrations, index, r)

class PointedDepolymerization(_FixedRate):
    __slots__ = []
    def __init__(self, **kwargs):
        _FixedRate.__init__(self, check_index=0, **kwargs)

    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]
        if not current_filament.states:
            _log.error('Attempted to depolymerize empty filament.')
        current_filament.shrink_pointed_end()
        concentrations[self.state].add_monomer(time)
        _FixedRate.perform(self, time, filaments, concentrations, index, r)
