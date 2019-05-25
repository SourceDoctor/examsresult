#!/bin/bash

export PYTHONPATH=/usr/lib/python3/dist-packages

rm -rf build
rm -rf examsresult.egg-info

python3 setup.py install -f

examsresult
