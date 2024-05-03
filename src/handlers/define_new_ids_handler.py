import datetime

from services.calculate_distance_between_two_points_service import calculate_distance_between_two_points


class DefineNewIds:
    def __init__(self, source_data, selected_poi_df, poi_name):
        self.poi_name = poi_name
        self.source_data = source_data
        max_id = self.get_max_id()
        self.new_ids_df = self.define_new_ids(selected_poi_df=selected_poi_df, max_id=max_id)

    def get_max_id(self):
        return self.source_data.poi_data_df['id_poi'].max()

    def define_new_ids(self, selected_poi_df, max_id):
        # Filter possible existing pois and define new ids
        existing_poi = self.source_data.poi_data_df.loc[self.source_data.poi_data_df['name'] == self.poi_name]
        if existing_poi.empty:
            name = self.poi_name
            type_name = list(selected_poi_df['label'])[0]
            subtype_name = list(selected_poi_df['label'])[0]
        else:
            name = existing_poi['name'].iloc[0]
            type_name = existing_poi['type_name'].iloc[0]
            subtype_name = existing_poi['subtype_name'].iloc[0]

        # Validate distance compare to existing poi
        if not existing_poi.empty:
            new_validated_ids = []
            for poi in selected_poi_df.index:
                selected_poi_row = selected_poi_df.loc[poi]
                for exi_poi in existing_poi.index:
                    existing_poi_row = existing_poi.loc[exi_poi]
                    distance = calculate_distance_between_two_points(point_lat1=existing_poi_row['lat'],
                                                                     point_long1=existing_poi_row['long'],
                                                                     point_lat2=selected_poi_row['latitude'],
                                                                     point_long2=selected_poi_row['longitude'])
                    if distance > 0.3:
                        new_validated_ids = new_validated_ids + [poi]
        # Filter only pois that are really new, not duplicates
        selected_poi_df = selected_poi_df.loc[selected_poi_df.index.isin(new_validated_ids)]

        new_ids_start = max_id + 1
        selected_poi_df['name'] = name
        selected_poi_df['type_name'] = type_name
        selected_poi_df['subtype_name'] = subtype_name
        selected_poi_df['data_source'] = 'mapy_cz'
        selected_poi_df['category'] = 'NA'
        selected_poi_df['last_update'] = datetime.date.today()
        selected_poi_df['kod_zsj_d'] = 999999
        selected_poi_df['weight'] = 5

        selected_poi_df.rename({'longitude': 'long', 'latitude': 'lat'}, inplace=True, axis=1)

        selected_poi_df = selected_poi_df[['type_name', 'subtype_name', 'name', 'category', 'data_source',
                                           'last_update', 'long', 'lat', 'kod_zsj_d', 'weight']]
        selected_poi_df['id_poi'] = range(new_ids_start, new_ids_start+len(selected_poi_df))
        selected_poi_df.set_index('id_poi', drop=True, inplace=True)

        return selected_poi_df

