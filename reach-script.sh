#!/bin/bash

echo 'Creating nex5 file with marker positions'
python post-dlc.py

echo 'Adding kinematics for reaching task'
python post-dlc-reach.py
