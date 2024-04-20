# Adwiro 2022
# Load all necessary data
import logging

import pandas as pd

from src.queries.handler.get_poi_dist_handler import GetPoiDistances
from src.queries.handler.get_source_billboard_data_handler import GetBillboardSourceData


class GetAllModelingData:
    """
    Load all necessary data for campaign optimization
    """

    def __init__(self):
        self.poi_data_df = GetPoiDistances().load_campaign_poi_ids_data()
        self.billboards_df = GetBillboardSourceData().load_campaign_billboard_source_data()

        logging.info(f'All data loaded.')
