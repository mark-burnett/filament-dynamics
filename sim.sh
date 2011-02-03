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
GROUP_NAME=""
CONFIG_COMMAND=""

USE_PATH=.:modules/

display_args() {
    echo "Options:"
    echo
    echo "    -d <directory>        IO dirctory."
    echo "    -o <filename>         Object Graph file."
    echo "    -a <filename>         Parameters file."
    echo "    -n <integer>          Number of processes."
    echo "    -g <group name>       Name of database group (required)."
    echo
}

typeset -i SIMNUM NUM_PROCESSES

let NUM_PROCESSES=1

while getopts "d:o:a:n:g:c:h" FLAG; do
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
            GROUP_NAME=$OPTARG;;
        "c")
            CONFIG_COMMAND="--config $OPTARG";;
        "h")
            display_args
            exit 0
    esac
done

#if [ -z $GROUP_NAME ]; then
#    display_args
#    exit 0
#fi

FULL_OBJECT_PATH="$DIRECTORY_NAME/$OBJECT_GRAPH_FILENAME"
FULL_PARAMETERS_PATH="$DIRECTORY_NAME/$PARAMETERS_FILENAME"

PYTHONPATH=$USE_PATH bin/create_jobs.py \
               --parameters       $FULL_PARAMETERS_PATH\
               --object_graph     $FULL_OBJECT_PATH\
               --group_name       "$GROUP_NAME"\
               $CONFIG_COMMAND || exit 1

for ((SIMNUM=1; SIMNUM <= NUM_PROCESSES; ++SIMNUM)); do
    PYTHONPATH=$USE_PATH bin/run_jobs.py $CONFIG_COMMAND &
done

wait

PYTHONPATH=$USE_PATH bin/cleanup_jobs.py $CONFIG_COMMAND
