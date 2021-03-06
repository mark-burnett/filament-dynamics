#!/usr/bin/env bash

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


# Configurable options
UNIT_TEST_COMMAND=bin/run_unit_tests.sh
INTEGRATION_TEST_COMMAND=bin/run_integration_tests.sh

DEFAULT_RUN_C_TESTS=true
DEFAULT_RUN_UNIT_TESTS=true
DEFAULT_RUN_INTEGRATION_TESTS=true

# Below this point is real code, not options.
RUN_C_TESTS=false
RUN_UNIT_TESTS=false
RUN_INTEGRATION_TESTS=false
ARGUMENTS_RECEIVED=false

LD_LIBRARY_PATH=./lib
export LD_LIBRARY_PATH

display_args() {
    echo "Options:"
    echo
    echo "    -a    Run all tests."
    echo
    echo "    -p    Run Python unit tests."
    echo "    -c    Run C++ unit tests."
    echo "    -i    Run integration tests."
    echo
    echo "    -h    Print this message."
    echo
}

run_c_tests() {
    echo "Running C++ Python unit..."
    pushd cpp_stochastic > /dev/null
    bjam -q runtests && ./runtests
    popd > /dev/null
    echo
}

run_unit_tests() {
    echo "Running Python unit tests..."
    $UNIT_TEST_COMMAND
    echo
}

run_integration_tests() {
    echo "Running integration tests..."
    $INTEGRATION_TEST_COMMAND
    echo
}

while getopts "acpih" FLAG; do
    case $FLAG in
        "a")
            ARGUMENTS_RECEIVED=true
            RUN_C_TESTS=true
            RUN_UNIT_TESTS=true
            RUN_INTEGRATION_TESTS=true
            break;;
        "c")
            ARGUMENTS_RECEIVED=true
            RUN_C_TESTS=true;;
        "p")
            ARGUMENTS_RECEIVED=true
            RUN_UNIT_TESTS=true;;
        "i")
            ARGUMENTS_RECEIVED=true
            RUN_INTEGRATION_TESTS=true;;
        "h")
            display_args
            exit 0
    esac
done

echo "Running automated tests."
echo

if $ARGUMENTS_RECEIVED; then
    if $RUN_C_TESTS; then
        run_c_tests
    fi
    if $RUN_UNIT_TESTS; then
        run_unit_tests
    fi

    if $RUN_INTEGRATION_TESTS; then
        run_integration_tests
    fi
else
    if $DEFAULT_RUN_C_TESTS; then
        run_c_tests
    fi

    if $DEFAULT_RUN_UNIT_TESTS; then
        run_unit_tests
    fi

    if $DEFAULT_RUN_INTEGRATION_TESTS; then
        run_integration_tests
    fi
fi

echo "Tests complete."
echo
