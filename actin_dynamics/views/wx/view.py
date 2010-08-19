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

import wx

from .main_frame import MainFrame

from .simulate_panel import SimulatePanel
from .analysis_panel import AnalysisPanel
from .fit_panel import FitPanel

from . import config


class wxView(object):
    def __init__(self, publisher, configobj):
        co = config.wxConfigObject.from_configobj(configobj['wx'])

        self.app = wx.PySimpleApp()

        self.main_frame = MainFrame(publisher=publisher, config=co,
                title='Actin Dynamics Stochastic Simulations',
                size=co.window_size)

        # The main panel is basically a notebook (with menu and status bars?)
        notebook = wx.Notebook(parent=self.main_frame)

        notebook.AddPage(SimulatePanel(publisher=publisher, parent=notebook,
                                       config=co), 'Simulation Browser')
        notebook.AddPage(AnalysisPanel(publisher=publisher, parent=notebook,
                                       config=co), 'Analyze')
        notebook.AddPage(FitPanel(publisher=publisher, parent=notebook,
                                  config=co), 'Fit Data')

    def display(self):
        self.main_frame.Show()
