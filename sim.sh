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
VIEW_LOG=true

display_args() {
    echo "Options:"
    echo
    echo "    -s <filename>         Session file to use."
    echo "    -c <filename>         Configuration file to use."
    echo "    -n <integer>          Number of worker processes."
    echo "    -l                    Do not show log."
    echo "    -j                    Do not create jobs, just complete them."
    echo "                              Note:  only '-n <integer>' argument used."
    echo
}

typeset -i SIMNUM NUM_PROCESSES

let NUM_PROCESSES=1

while getopts "s:n:c:jlh" FLAG; do
    case $FLAG in
        "s")
            SESSION_FILENAME=$OPTARG;;
        "c")
            CONFIG_COMMAND="--config $OPTARG";;
        "n")
            let NUM_PROCESSES=$OPTARG;;
        "j")
            CREATE_JOBS=false;;
        "l")
            VIEW_LOG=false;;
        "h")
            display_args
            exit 0
    esac
done

if $CREATE_JOBS; then
    echo
    echo "Creating jobs..."
    bin/controller.py $CONFIG_COMMAND $SESSION_FILENAME >& /dev/null &
fi

echo "Starting job runners..."
for ((SIMNUM=1; SIMNUM <= NUM_PROCESSES; ++SIMNUM)); do
    nice 5 bin/worker.py $CONFIG_COMMAND >& /dev/null &
    echo "Started process #$SIMNUM"
done

if $VIEW_LOG; then
    echo "Following log."
    bin/view_log.py -t -f $CONFIG_COMMAND

    trap 'exit 0' HUP
    trap 'kill -s HUP 0' EXIT
fi
