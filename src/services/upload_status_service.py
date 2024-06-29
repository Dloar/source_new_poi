import datetime
import logging

import pandas as pd

from handlers.create_db_connection import DbConnectorModel


def upload_status(status_results,
                  new_status: pd.DataFrame):
    logging.info('Distances loaded')

    new_status['state'] = status_results
    new_status['updated'] = datetime.datetime.today()
    del new_status['id']
    engine = DbConnectorModel().create_alchemy_db_connection(target_db='adwiro_web_dev')
    new_status.to_sql('adw_billboard_poi_dictionary', con=engine, if_exists='append', index=False)

    logging.info('Distances loaded')