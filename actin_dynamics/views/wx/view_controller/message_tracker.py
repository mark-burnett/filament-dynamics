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

class MessageTracker(object):
    def __init__(self, publisher, update_message, update_message_field,
                 request_message):
        self.update_message_field = update_message_field
        self.current_value = None

        publisher.subscribe(self.update, update_message)
        publisher.subscribe(self.request, request_message)

    def update(self, update_message):
        self.current_value = getattr(update_message, self.update_message_field,
                                     None)

    def request(self, request_message):
        request_message.callback(self.current_value)
