#!/bin/bash

export poi_brand=$1
export poi_group=$2
source /home/ubuntu/adwiro-proj/venv-adwiro/bin/activate

python3 /home/ubuntu/adwiro-proj/source_new_poi/src/__main__.py poi_brand poi_group