import logging
from typing import NoReturn

from commands.find_poi_on_name_handler import FindPoiOnNameHandler
from handlers.UploadPoiResultsHandler import UploadPoiResultsHandler
from handlers.calculate_poi_distances_handler import CalculatedPoiDistances
from handlers.define_new_ids_handler import DefineNewIds
from handlers.get_data_for_modeling_handler import GetAllModelingData

class RunModel:

    @staticmethod
    def run_model(poi_brand: str = '', poi_group: str = '') -> NoReturn:
        try:
            print(200)
        except:
            print(500)

        # Source poi ids and distances
        source_data = GetAllModelingData()
        # Find new pois based name
        # FindPoiOnNameHandler().define_gps_psc()
        new_selected_poi_df = FindPoiOnNameHandler().find_poi_on_name_handler(poi_brand=poi_brand, poi_group=poi_group)
        # Define new ids for the db
        new_poi_ids_df = DefineNewIds(source_data=source_data, poi_name=poi_brand, selected_poi_df=new_selected_poi_df)

        # # Calculate distances
        calculated_distances_df = CalculatedPoiDistances(source_data=source_data, poi_name=poi_brand,
                                                         selected_poi_df=new_poi_ids_df).define_new_poi_dataframe()

        UploadPoiResultsHandler(calculated_distances_df=calculated_distances_df,
                                new_ids_df=new_poi_ids_df.new_ids_df)
        logging.info('Model Finished')
