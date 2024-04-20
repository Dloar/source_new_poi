# Adwiro 2022
# Get billboard source data

class GetBillboardSourceDataQuery:
    @staticmethod
    def query_source_billboard_data(schema_name):
        query_source_billboard_data = f'''
                SELECT billboard_id, country, district, region, latitude, longitude
                FROM `{schema_name}`.adw_billboards 
                 ;'''

        return query_source_billboard_data
