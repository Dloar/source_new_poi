import json
import logging
from typing import AnyStr, NoReturn

import boto3
import mysql.connector
import numpy as np
import pandas as pd
from botocore.exceptions import ClientError

logging.getLogger('boto').setLevel(logging.CRITICAL)


def _get_secret(secret_name):
    region_name = 'eu-central-1'

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    try:
        secret = json.loads(secret)
    except:
        secret = secret.replace("\'", "\"")
        secret = json.loads(secret)
    return secret


def _diff_month(d1, d2):
    """
    months difference between two dates.
    :param d1:
    :param d2:
    :return:
    """
    return (d1.year - d2.year) * 12 + (d1.month - d2.month) + 1


def _is_number(int: AnyStr):
    """

    :param int:
    :return:
    """
    try:
        float(int)
        return True
    except ValueError:
        return False


def _sub_diac(string: AnyStr) -> AnyStr:
    """
        Substitude letters in word with diacritic.
    :return:
    """
    dictableSmall = list(u"ěščřžýáíéúůóťďň")
    nedictableSmall = list("escrzyaieuuotdn")
    dictableBig = list(u"ĚŠČŘŽÝÁÍÉÚŮÓŤĎŇ")

    vyslednyStr = ""
    try:
        if str(string) != 'nan':
            for znak in string:
                if not _is_number(znak):
                    if znak in dictableSmall:
                        vyslednyStr += nedictableSmall[dictableSmall.index(znak)]
                    elif znak in dictableBig:
                        vyslednyStr += nedictableSmall[dictableBig.index(znak)]
                    else:
                        vyslednyStr += znak
                else:
                    vyslednyStr += znak
            return vyslednyStr.lower()
        else:
            return np.nan
    except Exception as e:
        logging.info(f"Error: {e}")


def sub_month(month: AnyStr) -> int:
    """

    :param month:
    :return:
    """
    months_names = {'leden': 1, 'unor': 2, 'brezen': 3, 'duben': 4, 'kveten': 5, 'cerven': 6, 'cervenec': 7, 'srpen': 8,
                    'zari': 9, 'rijen': 10, 'listopad': 11, 'prosinec': 12}

    return (months_names[month])


def _adj_table(table: pd.DataFrame) -> pd.DataFrame:
    """

    :param table:
    :return:
    """
    columns = table.columns
    columns_adj = list()
    for index in range(len(columns)):
        columns_adj += [_sub_diac(columns[index])]

    table.columns = columns_adj

    for col in columns_adj:
        if table[col].dtype in ['object']:
            table[col] = table[col].apply(_sub_diac)

    return table


def _set_up_conn() -> NoReturn:
    """

    :return:
    """
    try:
        secret = _get_secret(secret_name='test/db/admin')
        conn = mysql.connector.connect(
            host=secret['host'],
            user=secret['username'],
            passwd=secret['password'],
            database=secret['dbInstanceIdentifier'],
            port=secret['port']
        )
        logging.info(' Database connection open.')
    except mysql.connector.Error as e:
        logging.info('Connection to the database is not possible')
        logging.info(e.args)
        raise

    return conn
