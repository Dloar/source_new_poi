import datetime
import logging
import os
import sys
import warnings

from src.commands.run_model_command import RunModel

if sys.platform == 'linux':
    poi_brand = os.environ["poi_brand"]
    poi_group = os.environ["poi_group"]
else:
    poi_brand = 'Kaufland'
    poi_group = ''

# set up parameters
FORMAT = '%(asctime)s: %(message)s'
logging.getLogger('boto').setLevel(logging.CRITICAL)


logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename=f'logging/{poi_brand}: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log')
warnings.filterwarnings("ignore")

startTime = datetime.datetime.now()
RunModel().run_model(poi_brand=poi_brand, poi_group=poi_group)

logging.info(f'Run time {datetime.datetime.now() - startTime} for id {poi_brand}')
