#!/usr/bin/env bash

echo 'Dropping old database.'
sudo -u postgres dropdb actin_dynamics

echo 'Creating new database.'
sudo -u postgres createdb -O aduser actin_dynamics

echo 'Creating tables.'
python tools/create_tables.py

echo 'Creating test data.'
python tools/create_test_data.py
