#!/usr/bin/env bash

set -e

cd data
./produce_data.py
cd ../

cd plotter
./example.py
cd ../

cd school
./tuning.py
./learning.py
./working.py
cd ../

cd statistics
./fit.py
./upper_bound.py
./significance.py
cd ../

exit 0
