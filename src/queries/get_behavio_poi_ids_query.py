# Adwiro 2022
# Get billboard source data

class GetPoiBehavioData:
    def __init__(self, schema_name):
        """

        :param schema_name: table db schema
        """
        self.schema_name = schema_name

    def query_poi_behavio_dict(self, selected_ids):
        """
        load all available distances for selected pois and available boards
        :param poi_list: list of selected pois
        :param hash_list: list of selected boards ids
        :return:
        """
        query_poi_behavio_ids_data = f'''
                SELECT id_poi, id_behavio
                FROM `{self.schema_name}`.adw_behavio_dict
                WHERE id_behavio in {tuple(selected_ids)}
                 ;'''
        return query_poi_behavio_ids_data

    def query_poi_behavio_distance(self, behavio_tags):
        query_poi_behavio_dist_data = f'''
                SELECT id_behavio, tag, label, label_search, description, extra_tooltip, category
                FROM `{self.schema_name}`.adw_behavio_poi_ids
                WHERE tag in {behavio_tags}
                 ;'''

        return query_poi_behavio_dist_data
