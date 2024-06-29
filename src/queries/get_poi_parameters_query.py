# Adwiro 2022
# Get billboard source data

class GetPoiParametersData:

    def query_poi_parameters_query(self,
                                   new_poi_id,
                                   schema_name):
        """

        :param selected_ids:
        :return:
        """
        query_poi_behavio_ids_data = f'''
                SELECT  id, name, state, created, updated
                FROM `{schema_name}`.adw_billboard_poi_dictionary
                WHERE id = {new_poi_id}
                 ;'''
        return query_poi_behavio_ids_data
