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


OBJECT_GRAPH_FILENAME="object_graph.yaml"
PARAMETERS_FILENAME="parameters.yaml"
DIRECTORY_NAME="."
NUM_SIMULATIONS="1"

SPLIT_COMMAND=""
CONFIG_COMMAND=""

DIR_NAME_AS_GROUP_NAME=true
CREATE_JOBS=true

typeset -i BASE_DELAY
let BASE_DELAY=5

USE_PATH=.:modules/

display_args() {
    echo "Options:"
    echo
    echo "    -d <directory>        IO dirctory."
    echo "    -o <filename>         Object Graph file."
    echo "    -a <filename>         Parameters file."
    echo "    -n <integer>          Number of processes."
    echo "    -g <group name>       Name of database group (required)."
    echo "    -j                    Do not create jobs, just complete them."
    echo "                              Note:  only '-n <integer>' argument used."
    echo
}

typeset -i SIMNUM NUM_PROCESSES

let NUM_PROCESSES=1

while getopts "d:o:a:n:g:c:jh" FLAG; do
    case $FLAG in
        "d")
            DIRECTORY_NAME=$OPTARG;;
        "o")
            OBJECT_GRAPH_FILENAME=$OPTARG;;
        "a")
            PARAMETERS_FILENAME=$OPTARG;;
        "n")
            let NUM_PROCESSES=$OPTARG;;
        "g")
            DIR_NAME_AS_GROUP_NAME=false
            GROUP_NAME=$OPTARG;;
        "c")
            CONFIG_COMMAND="--config $OPTARG";;
        "j")
            CREATE_JOBS=false;;
        "h")
            display_args
            exit 0
    esac
done

#if [ -z $GROUP_NAME ]; then
#    display_args
#    exit 0
#fi

if $DIR_NAME_AS_GROUP_NAME; then
    GROUP_NAME=$DIRECTORY_NAME
fi

echo "Starting job runners..."
for ((SIMNUM=1; SIMNUM <= NUM_PROCESSES; ++SIMNUM)); do
    DELAY=$((BASE_DELAY + SIMNUM))
    PYTHONPATH=$USE_PATH bin/run_jobs.py --delay $DELAY $CONFIG_COMMAND &
    echo "Started process #$SIMNUM"
done

if $CREATE_JOBS; then
    echo
    echo "Creating jobs..."
    FULL_OBJECT_PATH="$DIRECTORY_NAME/$OBJECT_GRAPH_FILENAME"
    FULL_PARAMETERS_PATH="$DIRECTORY_NAME/$PARAMETERS_FILENAME"

    PYTHONPATH=$USE_PATH bin/create_jobs.py \
                   --parameters       $FULL_PARAMETERS_PATH\
                   --object_graph     $FULL_OBJECT_PATH\
                   --group_name       "$GROUP_NAME"\
                   $CONFIG_COMMAND || exit 1
    echo "Jobs created."
fi

echo "Waiting to complete..."


wait

echo "Cleaning up unfinished jobs..."
PYTHONPATH=$USE_PATH bin/cleanup_jobs.py $CONFIG_COMMAND
