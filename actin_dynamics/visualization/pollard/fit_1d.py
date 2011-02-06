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

from .. import themes
from .. import variation

def adppi(group, theme=None):
    if not theme:
        theme = themes.Variation()

    theme.initialize()

    variation.run_val_vs_par(group, abscissa='cleavage_rate',
                   ordinate='pollard_adppi_chi_squared',
                   label='Cleavage Rate', theme=theme)

    variation.run_val_vs_par(group, abscissa='filament_tip_concentration',
                   ordinate='pollard_adppi_chi_squared',
                   label='FTC', theme=theme)

    theme.finalize()
