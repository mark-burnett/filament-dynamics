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

from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor

# NOTE This moneky patch taken from twisted ticket # 3948
# Monkey-patch the wxreactor to make it exit correctly.
if wxreactor.WxReactor.callFromThread is not None:
    oldStop = wxreactor.WxReactor.stop
    def stopFromThread(self):
        self.callFromThread(oldStop, self)
    wxreactor.WxReactor.stop = stopFromThread


import signal
import views
from actin_dynamics import presenters
from actin_dynamics.common.publisher import Publisher


# XXX this is so that we can use the publisher in the wx.py.shell
publisher = Publisher()
def go(config):

    view = views.wxView(publisher, config)

    uh = presenters.ui_handler.GUIHandler(publisher)
    ph = presenters.process_handler.MultiprocessHandler(publisher)
    presenter = presenters.Presenter(publisher, [uh, ph])

    # Presenter initialize function makes construction order unimportant.
    presenter.initialize()
    view.display()

    reactor.registerWxApp(view.app)

# XXX There must be some way to catch CTRL-C properly with this setup.
#    def handle_control_c(a, b):
#        print 'did i get here?'
#        publisher.publish(presenters.messages.ExitProgram('Keyboard Interrupt'))
#    signal.signal(signal.SIGINT, handle_control_c)

    reactor.run()
