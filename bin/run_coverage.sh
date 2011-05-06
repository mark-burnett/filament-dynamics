#!/usr/bin/env bash

rm .coverage
coverage run --branch /usr/local/lib/python2.6/dist-packages/discover.py -s unit_tests/ > /dev/null >& /dev/null
coverage report
