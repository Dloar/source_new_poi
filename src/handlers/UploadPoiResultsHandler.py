from handlers.create_db_connection import DbConnectorModel


class UploadPoiResultsHandler:
    def __init__(self, calculated_distances_df, new_ids_df):
        self.upload_poi_ids_results(new_ids_df=new_ids_df)
        self.upload_poi_dist_results(calculated_distances_df=calculated_distances_df)

    def upload_poi_ids_results(self, new_ids_df):
        # 2533241
        new_ids_df.reset_index(drop=False, inplace=True)
        engine = DbConnectorModel().create_alchemy_db_connection()
        new_ids_df.to_sql('adw_poi_ids', con=engine, if_exists='append', index=False)
    def upload_poi_dist_results(self, calculated_distances_df):
        engine = DbConnectorModel().create_alchemy_db_connection()
        calculated_distances_df.to_sql('adw_poi_dist', con=engine, if_exists='append', index=False)
