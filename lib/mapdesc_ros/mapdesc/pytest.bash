#!/bin/bash
# run pytest and coverage
python3 -m coverage run --source mapdesc -m pytest .
python3 -m coverage report -m
python3 -m coverage html