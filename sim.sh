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


OBJECT_GRAPH_FILENAME="object_graph.yaml"
PARAMETERS_FILENAME="parameters.yaml"
DIRECTORY_NAME="."
NUM_SIMULATIONS="1"
SPLIT_COMMAND=""
GROUP_NAME=""

display_args() {
    echo "Options:"
    echo
    echo "    -d <directory>        IO dirctory."
    echo "    -o <filename>         Object Graph file."
    echo "    -a <filename>         Parameters file."
    echo "    -n <integer>          Number of processes."
    echo "    -s <integer>          Number of simulations per par set."
    echo "    -p <parameter_name>   Name of parameter for splitting up work."
    echo "    -g <group name>       Name of database group (required)."
    echo
}

typeset -i SIMNUM NUM_PROCESSES

let NUM_PROCESSES=1

while getopts "d:o:a:n:s:p:g:h" FLAG; do
    case $FLAG in
        "d")
            DIRECTORY_NAME=$OPTARG;;
        "o")
            OBJECT_GRAPH_FILENAME=$OPTARG;;
        "a")
            PARAMETERS_FILENAME=$OPTARG;;
        "n")
            let NUM_PROCESSES=$OPTARG;;
        "s")
            let NUM_SIMULATIONS=$OPTARG;;
        "p")
            SPLIT_COMMAND="--split_parameter $OPTARG";;
        "g")
            GROUP_NAME=$OPTARG;;
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

for ((SIMNUM=1; SIMNUM <= NUM_PROCESSES; ++SIMNUM)); do
    PYTHONPATH=. bin/cli.py --object_graph     $FULL_OBJECT_PATH\
               --parameters       $FULL_PARAMETERS_PATH\
               --group_name       "$GROUP_NAME"\
               --num_sims         $NUM_SIMULATIONS\
               --process_number   $SIMNUM\
               --num_processes    $NUM_PROCESSES\
               $SPLIT_COMMAND &
done

wait
