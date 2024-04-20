import mpu
import pandas as pd

from services.calculate_distance_between_two_points_service import calculate_distance_between_two_points


class CalculatedPoiDistances:
    def __init__(self, source_data, selected_poi_df, poi_name):
        self.source_data = source_data
        self.poi_name = poi_name
        self.valid_distance_list = self.calculate_distances(billboard_df=source_data.billboards_df,
                                                            selected_poi_df=selected_poi_df)
    @staticmethod
    def calculate_distances(billboard_df, selected_poi_df, valid_distance_list=None):
        # Define mutable variable
        if valid_distance_list is None:
            valid_distance_list = list()

        # iterate over new pois and calculated distance
        try:
            for new_poi in selected_poi_df.new_ids_df.index:
                selected_poi = selected_poi_df.new_ids_df.loc[new_poi]
                for billboard in billboard_df.index:
                    selected_board = billboard_df.iloc[billboard]
                    if (selected_board['latitude'] is None) | (selected_board['longitude'] is None) | (
                            selected_board['latitude'] == '') | (selected_board['longitude'] == ''):
                        continue
                    distance = calculate_distance_between_two_points(point_lat1=selected_poi['lat'],
                                                                     point_long1=selected_poi['long'],
                                                                     point_lat2=selected_board['latitude'],
                                                                     point_long2=selected_board['longitude'])
                    if distance > 5:
                        continue
                    valid_distance_list = valid_distance_list + [{'poi_index': new_poi,
                                                                  'billboard_id': selected_board['billboard_id'],
                                                                  'distance': distance}]
                print(f'All boards done for {new_poi}')
        except:
            pass
        return valid_distance_list

    def define_new_poi_dataframe(self):
        # Convert results in the dataframe
        calculated_distances_df = pd.DataFrame(self.valid_distance_list)
        calculated_distances_df['distance'] = calculated_distances_df['distance'] * 1000
        calculated_distances_df.rename({'billboard_id': 'id_hash', 'poi_index': 'id_poi'}, axis=1, inplace=True)

        return calculated_distances_df
