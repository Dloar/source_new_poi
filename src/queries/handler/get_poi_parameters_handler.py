# Adwiro 2022
# Load campaign parameters
import logging

import pandas as pd

from handlers.create_db_connection import DbConnectorModel
from queries.get_poi_parameters_query import GetPoiParametersData


class GetPoiParametersDataHandler:
    @staticmethod
    def load_poi_parameters_data(new_poi_id):
        conn_engine = DbConnectorModel()
        db_conn = conn_engine.create_db_connection()
        new_poi_parameters = pd.read_sql_query(
            GetPoiParametersData().query_poi_parameters_query(schema_name='adwiro_web_dev', new_poi_id=new_poi_id),
            db_conn)

        db_conn.close()

        return new_poi_parameters
