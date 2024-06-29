# Adwiro 2022
# Load database secrets and create connection

import mysql
from sqlalchemy import create_engine


from handlers.get_config_parameters import ParFactory
from services.support_functions import _get_secret


class DbConnectorModel:
    def __init__(self):
        par_factory_var: ParFactory = ParFactory()
        self.secrets = _get_secret(secret_name=par_factory_var.return_secret_name())

    def create_db_connection(self) -> object:
        conn = mysql.connector.connect(
            host=self.secrets['host'],
            user=self.secrets['username'],
            passwd=self.secrets['password'],
            database=self.secrets['dbInstanceIdentifier'],
            port=self.secrets['port']
        )
        return conn

    def create_alchemy_db_connection(self, target_db=None) -> object:

        if target_db:
            engine = create_engine(
                f"mysql+mysqlconnector://{self.secrets['username']}:{self.secrets['password']}@{self.secrets['host']}/{target_db}",
                echo=False)
        else:
            engine = create_engine(
                f"mysql+mysqlconnector://{self.secrets['username']}:{self.secrets['password']}@{self.secrets['host']}/{self.secrets['dbInstanceIdentifier']}",
                echo=False)

        return engine
