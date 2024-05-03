#!/bin/bash

export poi_brand=$1
export poi_group=$2
source /home/ubuntu/adwiro-proj/venv-adwiro/bin/activate
export PYTHONPATH=${PYTHONPATH}:~/adwiro-proj

cd /home/ubuntu/adwiro-proj/source_new_poi/src

python3 __main__.py poi_brand poi_group