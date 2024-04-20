# Adwiro 2022
# Get billboard source data
import json


class GetPoiSourceData:
    @staticmethod
    def query_poi_distance_data(poi_list, schema_name, hash_list, distance_limit):
        """
        load all available distances for selected pois and available boards
        :param poi_list: list of selected pois
        :param schema_name: table db schema
        :param hash_list: list of selected boards ids
        :param distance_limit: limit of the distance for given campaign
        :return:
        """
        query_poi_distance_data = f'''
                SELECT id_hash, id_poi, distance
                FROM `{schema_name}`.adw_poi_dist
                WHERE id_poi in {poi_list} and id_hash in {hash_list} and distance <= {distance_limit}
                 ;'''
        return query_poi_distance_data


    @staticmethod
    def query_poi_ids_data(schema_name):
        query_poi_ids_data = f'''
                SELECT type_name, subtype_name, name, `long`, lat, id_poi
                FROM `{schema_name}`.adw_poi_ids
                 ;'''

        return query_poi_ids_data


