import logging
import boto3
from botocore.exceptions import ClientError

from ..lib.exception import AwsErrorException
from ..models.table import Table, Column


logger = logging.getLogger(__name__)

def get_table_count(db_name):

    glue_client = boto3.client('glue')

    table_count = 0

    try:
        logger.debug(f"getting the table count for database {db_name}")
        resp = glue_client.get_tables(DatabaseName=db_name)

        table_count = table_count + len(resp['TableList'])

        while 'NextToken' in resp:
            logger.debug("getting additional tables from the pagination")
            resp = glue_client.get_tables(DatabaseName=db_name, NextToken=resp['NextToken'])

            table_count = table_count + len(resp['TableList'])

    except ClientError as e:
        logger.error(f"error getting the list of tables for db {db_name}: {e}")
        raise AwsErrorException

    return table_count


def get_page_of_tables(db_name, page_num, page_amount):

    glue_client = boto3.client('glue')

    table_list = []

    resp = glue_client.get_tables(DatabaseName=db_name, MaxResults=page_amount)
   
    if page_num is not 1:
        logger.debug("getting additional pages")
        i = 1

        while i is not page_num:
            i += 1
            logger.debug(f"getting page {i}")
        
            resp = glue_client.get_tables(
                    DatabaseName=db_name,
                    MaxResults=page_amount,
                    NextToken=resp['NextToken'])

    for table in resp['TableList']:
        
        logger.debug(f"processing table {table['Name']}")

        table_list.append(Table(table['Name'], table['Description'], table['UpdateTime']))


    return table_list

def get_table(db_name, table_name):

    glue_client = boto3.client('glue')

    resp = glue_client.get_table(DatabaseName=db_name, Name=table_name)

    table = Table(resp['Table']['Name'], resp['Table']['Description'], resp['Table']['UpdateTime'])
    column_list = []

    for col in resp['Table']['StorageDescriptor']['Columns']:

        column_list.append(Column(col['Name'], col['Type'], col['Comment']))

    table.set_column_list(column_list)

    return table

    


    


