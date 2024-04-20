# Adwiro 2022
# Load available boards
import logging

import pandas as pd

from adwiro.src.queries.get_poi_data_query import GetPoiSourceData
from adwiro.src.services.create_db_connection import DbConnectorModel
from adwiro.src.services.filter_boards_by_poi_name_filter_fun import filter_poi_by_name


class GetPoiFilteredIds:

    def __init__(self, schema_name, camp_parr_class: object):
        self.schema_name = schema_name
        self.camp_parr_class = camp_parr_class

    def load_campaign_ids(self, behavio_keys):

        conn_engine = DbConnectorModel()
        db_conn = conn_engine.create_db_connection()
        if self.camp_parr_class.target_type not in [1, 4]:
            if len(behavio_keys) == 0:
                campaign_poi_ids_data = pd.DataFrame(columns=["type_name", "subtype_name", "name",
                                                              "long", "lat", "id_poi"])
            else:
                campaign_poi_ids_data = pd.DataFrame(columns=["type_name", "subtype_name", "name",
                                                              "long", "lat", "id_poi"])
                # campaign_poi_ids_data = pd.read_sql_query(
                #     GetPoiSourceData().query_poi_ids_data(schema_name=self.schema_name, behavio_keys=behavio_keys),
                #     db_conn)
        else:
            campaign_poi_ids_data = pd.read_sql_query(
                GetPoiSourceData().query_poi_ids_limit_data(schema_name=self.schema_name,
                                                            camp_parr_class=self.camp_parr_class), db_conn)
        db_conn.close()

        # Filter boards based on the poi name fot the campaign 4
        if self.camp_parr_class.target_type == 4:
            if ((not all(self.camp_parr_class.billboards_poi['name'].unique() == '')) &
                    (not pd.isnull(self.camp_parr_class.billboards_poi['name']).all())):
                campaign_poi_ids_data = filter_poi_by_name(camp_parr_class=self.camp_parr_class,
                                                           campaign_poi_ids_data=campaign_poi_ids_data)

        logging.info(f'POI filter applied for brands: ({campaign_poi_ids_data.name.unique()})')
        return campaign_poi_ids_data
