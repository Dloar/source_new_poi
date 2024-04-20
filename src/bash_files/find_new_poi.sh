#!/bin/bash

export poi_brand=$1
export poi_group=$2
source /home/ubuntu/adwiro-proj/source_new_poi/venv/bin/activate
export PYTHONPATH=${PYTHONPATH}:~/adwiro-proj

python3 /home/ubuntu/adwiro-proj/source_new_poi/src/command/__main__.py poi_brand poi_group