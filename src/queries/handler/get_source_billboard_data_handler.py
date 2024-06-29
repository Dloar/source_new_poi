# Adwiro 2022
# Load campaign parameters
import logging

import pandas as pd

from handlers.create_db_connection import DbConnectorModel
from queries.get_campaign_billboard_data_query import GetBillboardSourceDataQuery


class GetBillboardSourceData:
    @staticmethod
    def load_campaign_billboard_source_data():
        conn_engine = DbConnectorModel()
        db_conn = conn_engine.create_db_connection()
        campaign_billboard_source_data = pd.read_sql_query(
            GetBillboardSourceDataQuery.query_source_billboard_data(schema_name='adwiro_web_dev'), db_conn)

        db_conn.close()



        return campaign_billboard_source_data
