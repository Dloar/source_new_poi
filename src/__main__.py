import datetime
import logging
import os
import sys
import warnings

from commands.run_model_command import RunModel

if sys.platform == 'linux':
    poi_id = os.environ["poi_id"]
else:
    poi_id = 6

FORMAT = '%(asctime)s: %(message)s'
logging.getLogger('boto').setLevel(logging.CRITICAL)

# Create a drectory for logging
newpath = f'{os.getcwd()}/POI-{poi_id}'
if not os.path.exists(newpath):
    os.makedirs(newpath)

logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename=f'{newpath}/{poi_id}: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log')
warnings.filterwarnings("ignore")

startTime = datetime.datetime.now()
RunModel().run_model(new_poi_id=poi_id)

logging.info(f'Run time {datetime.datetime.now() - startTime} for id {poi_id}')
