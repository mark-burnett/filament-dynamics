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
import wx.py

from .main_frame import MainFrame

from .analysis_panel import AnalysisPanel
from .fit_panel import FitPanel
from .simulate_panel import SimulatePanel
from .view_controller import ViewController

from . import config

from actin_dynamics.presenters import messages as presenter_messages
from . import messages as view_messages


class wxView(object):
    def __init__(self, publisher, configobj):
        co = config.wxConfigObject.from_configobj(configobj['wx'])
        self.view_controller = ViewController.from_configobj(
                publisher=publisher,
                configobj=configobj['wx']['view_controller'])

        # You must use PySimpleApp for things to display properly on OS X
        self.app = wx.PySimpleApp(clearSigInt=False)

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

        shell_locals = {'publisher': publisher,
                        'view_controller': self.view_controller,
                        'view_messages': view_messages,
                        'presenter_messages': presenter_messages}
        notebook.AddPage(wx.py.shell.Shell(locals=shell_locals,
                                           parent=notebook),
                         'Shell')

    def display(self):
        self.main_frame.Show()
