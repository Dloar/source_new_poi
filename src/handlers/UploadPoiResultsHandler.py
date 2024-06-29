import datetime
import logging

import pandas as pd

from handlers.create_db_connection import DbConnectorModel


class UploadPoiResultsHandler:
    def __init__(self,
                 calculated_distances_df: pd.DataFrame,
                 new_ids_df: pd.DataFrame,
                 new_status: pd.DataFrame):
        self.new_status = new_status

        try:
            self.upload_poi_ids_results(new_ids_df=new_ids_df)
            self.upload_poi_dist_results(calculated_distances_df=calculated_distances_df)
            self.upload_status(status_results=1)
        except:
            self.upload_status(status_results=2)

    def upload_poi_ids_results(self, new_ids_df):
        new_ids_df.reset_index(drop=False, inplace=True)
        engine = DbConnectorModel().create_alchemy_db_connection()
        new_ids_df.to_sql('adw_poi_ids', con=engine, if_exists='append', index=False)
        logging.info('Ids loaded')

    def upload_poi_dist_results(self, calculated_distances_df):
        engine = DbConnectorModel().create_alchemy_db_connection()
        calculated_distances_df.to_sql('adw_poi_dist', con=engine, if_exists='append', index=False)
        logging.info('Distances loaded')

    def upload_status(self, status_results):
        logging.info('Distances loaded')

        self.new_status['state'] = status_results
        self.new_status['updated'] = datetime.datetime.today()
        del self.new_status['id']
        engine = DbConnectorModel().create_alchemy_db_connection(target_db='adwiro_web_dev')
        self.new_status.to_sql('adw_billboard_poi_dictionary', con=engine, if_exists='append', index=False)

        logging.info('Distances loaded')
