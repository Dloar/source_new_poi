import logging

import requests
import pandas as pd
import yaml
import os


class FindPoiOnNameHandler():
    def __init__(self, ):
        with open('config/config.yaml') as config:
            country_parts_config = yaml.safe_load(config)

        self.districts = country_parts_config['model_parameters']['country_districts']
        self.regions = country_parts_config['model_parameters']['regions']
        self.psc = country_parts_config['model_parameters']['psc']
        self.apikey = country_parts_config['api_ident']['apikey']


    # def define_gps_psc(self):
    #     psc_list =  []
    #     for psc in self.psc:
    #         print(f'Running for {psc}')
    #
    #         api_url = f"""https://api.mapy.cz/v1/suggest?lang=cs&apikey=Cj3uvTKe2gZw3GZrM0Cq4WhasnpABreTzk4YXJoG9yo&query={psc}&limit=5&type=regional.municipality_part"""
    #         response = requests.get(api_url)
    #         response_run = response.json()
    #         try:
    #             output_df = pd.DataFrame(response_run['items'])
    #             if output_df.empty:
    #                 continue
    #             else:
    #                 if output_df['regionalStructure'][0][4]['isoCode'] == 'CZ':
    #                     print(output_df)
    #                     psc_list = psc_list + [psc]
    #         except:
    #             print(f'Fail {psc}')
    #
    #     breakpoint()

    def find_poi_on_name_handler(self, source_data,  limit='15'):

        selected_poi_df = pd.DataFrame(columns=['name', 'label', 'position', 'location'])#
        poi_brand = ''
        poi_name = source_data.poi_params.iloc[0]['name']
        lower_poi_name = poi_name.lower()
        for districts in self.districts:
            try:
                logging.info(f'Running for {districts}')

                api_url = f"""https://api.mapy.cz/v1/suggest?lang=cs&apikey={self.apikey}&query={lower_poi_name}&limit={limit}&locality={districts}"""
                response = requests.get(api_url)
                response_run = response.json()
                output_df = pd.DataFrame(response_run['items'])

                if output_df.empty:
                    logging.info(f'{districts} ends with no additional findings.')
                    continue
                else:
                    if poi_brand == '':
                        output_df = output_df[['name', 'label', 'position', 'location']]
                    else:
                        output_df['name_lower'] = output_df['name'].apply(lambda x: x.lower())
                        output_df = output_df.loc[output_df['name_lower'] == lower_poi_name][['name', 'label',
                                                                                              'position', 'location']]
                    selected_poi_df = pd.concat([selected_poi_df, output_df], axis=0)
                    logging.info(f'{districts} ends with {output_df.shape[0]}')
            except:
                logging.info(f'Exception triggered for {districts}')
                logging.info(response_run)

        selected_poi_df['longitude'] = selected_poi_df['position'].apply(lambda x: x['lon'])
        selected_poi_df['latitude'] = selected_poi_df['position'].apply(lambda x: x['lat'])
        selected_poi_df.drop('position', inplace=True, axis=1)
        selected_poi_df.drop_duplicates(inplace=True)
        selected_poi_df.reset_index(drop=True, inplace=True)

        logging.info(f'For {poi_name}, the model found {selected_poi_df.shape[0]} places')
        return selected_poi_df, poi_name, poi_brand
