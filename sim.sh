#!/usr/bin/env bash

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


SESSION_FILENAME=""

SPLIT_COMMAND=""
CONFIG_COMMAND=""

CREATE_JOBS=true

USE_PATH=.:modules/

display_args() {
    echo "Options:"
    echo
    echo "    -s <filename>         Session file to use."
    echo "    -c <filename>         Configuration file to use."
    echo "    -n <integer>          Number of worker processes."
    echo "    -j                    Do not create jobs, just complete them."
    echo "                              Note:  only '-n <integer>' argument used."
    echo
}

typeset -i SIMNUM NUM_PROCESSES

let NUM_PROCESSES=1

while getopts "s:n:c:jh" FLAG; do
    case $FLAG in
        "s")
            SESSION_FILENAME=$OPTARG;;
        "c")
            CONFIG_COMMAND="--config $OPTARG";;
        "n")
            let NUM_PROCESSES=$OPTARG;;
        "j")
            CREATE_JOBS=false;;
        "h")
            display_args
            exit 0
    esac
done

echo "Starting job runners..."
for ((SIMNUM=1; SIMNUM <= NUM_PROCESSES; ++SIMNUM)); do
    PYTHONPATH=$USE_PATH bin/worker.py $CONFIG_COMMAND &
    echo "Started process #$SIMNUM"
done

if $CREATE_JOBS; then
    echo
    echo "Creating jobs..."
    PYTHONPATH=$USE_PATH bin/controller.py $CONFIG_COMMAND\
        $SESSION_FILENAME || exit 1
    echo "Jobs created."
fi

echo "Waiting to complete..."
wait
