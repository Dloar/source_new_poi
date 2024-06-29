# Adwiro 2022
# Load all necessary data
import logging

import pandas as pd

from queries.handler.get_poi_dist_handler import GetPoiDistances
from queries.handler.get_poi_parameters_handler import GetPoiParametersDataHandler
from queries.handler.get_source_billboard_data_handler import GetBillboardSourceData


class GetAllModelingData:
    """
    Load all necessary data for campaign optimization
    """

    def __init__(self, new_poi_id):
        self.poi_params = GetPoiParametersDataHandler().load_poi_parameters_data(new_poi_id=new_poi_id)
        self.poi_data_df = GetPoiDistances().load_campaign_poi_ids_data(filter_name=self.poi_params['name'].iloc[0])
        self.billboards_df = GetBillboardSourceData().load_campaign_billboard_source_data()

        logging.info(f'All data loaded.')
