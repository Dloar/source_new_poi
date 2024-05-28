# Adwiro 2022
# Load config file from S3 Bucket
import os
from typing import Dict

import boto3
import yaml


class ParFactory:
    def __init__(self) -> Dict:
        """

        :rtype: object
        """

        s3_client = boto3.client('s3')
        bucket = 'ad-model-par'
        adwiro_env = 'dev'
        response = s3_client.get_object(Bucket=bucket, Key=f"model-config/{adwiro_env}/config.yaml")
        self.configfile = yaml.safe_load(response["Body"])

    def return_secret_name(self):
        secret_name = self.configfile['db_parameters']['secret_name']
        return secret_name

    def return_model_parameters(self):
        return self.configfile['model_parameters']

    def return_db_names(self):
        return [self.configfile['db_parameters']['web_db'], self.configfile['db_parameters']['backend_db']]

    def return_poi_keys(self):
        return self.configfile['poi_parameters']['category_of_interest']
