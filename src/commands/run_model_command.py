import logging
from typing import NoReturn

from commands.find_poi_on_name_handler import FindPoiOnNameHandler
from handlers.UploadPoiResultsHandler import UploadPoiResultsHandler
from handlers.calculate_poi_distances_handler import CalculatedPoiDistances
from handlers.define_new_ids_handler import DefineNewIds
from handlers.get_data_for_modeling_handler import GetAllModelingData
from services.upload_status_service import upload_status


class RunModel:

    def run_model(self,
                  new_poi_id) -> NoReturn:
        try:
            print(200)
        except:
            print(500)

        # Source poi ids and distances
        source_data = GetAllModelingData(new_poi_id=new_poi_id)
        logging.info('Data loaded')
        # Find new pois based name
        # FindPoiOnNameHandler().define_gps_psc()
        new_selected_poi_df, poi_name, poi_brand = FindPoiOnNameHandler().find_poi_on_name_handler(source_data=source_data)
        logging.info('New poi discovered')
        # Define new ids for the db
        new_poi_ids_df = DefineNewIds(source_data=source_data, poi_name=poi_name, selected_poi_df=new_selected_poi_df)
        logging.info('New ids assign')

        if new_poi_ids_df.new_ids_df.empty:
            # Upload status if no new ids are discovered
            upload_status(new_status=source_data.poi_params, status_results=3)
            exit()
        # # Calculate distances
        calculated_distances_df = CalculatedPoiDistances(source_data=source_data, poi_name=poi_name,
                                                         selected_poi_df=new_poi_ids_df).define_new_poi_dataframe()
        logging.info(f'New distances calculated for {calculated_distances_df.shape[0]}')

        UploadPoiResultsHandler(calculated_distances_df=calculated_distances_df,
                                new_ids_df=new_poi_ids_df.new_ids_df, new_status=source_data.poi_params)

        logging.info('Model Finished')
