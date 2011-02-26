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

import unittest

import sys, traceback
import logging

from actin_dynamics import database

from unit_tests.database.base_test_cases import DBTestCase


# XXX This test case doesn't really need a db_session..
class TestTraceback(DBTestCase):
    def test_construction(self):
        try:
            raise RuntimeError('Traceback construction test.')
        except:
            tb = sys.exc_info()[2]

        t = database.DBTraceback(*traceback.extract_tb(tb)[0])

        self.assertTrue(t.lineno > 0)
        self.assertEqual(t.line,
            "raise RuntimeError('Traceback construction test.')")


# XXX This test case doesn't really need a db_session..
class TestException(DBTestCase):
    def test_construction(self):
        try:
            raise RuntimeError('Exception construction test.')
        except:
            ei = sys.exc_info()
            e = database.DBException(type=ei[0], value=ei[1], traceback=ei[2])

        self.assertEqual(1, len(e.traceback))
        self.assertEqual('RuntimeError', e.type_name)
        self.assertEqual('Exception construction test.', e.message)


# XXX This test case doesn't really need a db_session..
class TestLogRecord(DBTestCase):
    def test_construction(self):
        try:
            raise RuntimeError('LogRecord construction test.')
        except:
            lr = logging.LogRecord('name', 20, 'pathname', 7,
                                   'msg %s', ('a',),
                                   sys.exc_info(), func=self.test_construction)

        dblr = database.DBLogRecord.from_LogRecord(lr)

        self.assertEqual(7, dblr.lineno)
        self.assertEqual('INFO', dblr.levelname)
        self.assertEqual('msg a', dblr.message)
        self.assertEqual('pathname', dblr.pathname)
        self.assertEqual('name', dblr.name)

        self.assertTrue(dblr.exception is not None)
        self.assertEqual(1, len(dblr.exception.traceback))


if '__main__' == __name__:
    unittest.main()
