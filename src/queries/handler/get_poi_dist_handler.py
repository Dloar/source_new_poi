# Adwiro 2022
# Load available boards
import logging

import pandas as pd

from handlers.create_db_connection import DbConnectorModel
from queries.get_poi_data_query import GetPoiSourceData


class GetPoiDistances:

    @staticmethod
    def load_campaign_poi_ids_data():
        """

        :return:
        """
        # Necessary to rebuild the source process
        conn_engine = DbConnectorModel()
        db_conn = conn_engine.create_db_connection()
        campaign_poi_data = pd.read_sql_query(
            GetPoiSourceData.query_poi_ids_data(schema_name='adwiro-db-dev'),
            db_conn)
        db_conn.close()

        return campaign_poi_data
