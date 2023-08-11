import logging
import boto3
from botocore.exceptions import ClientError

from ..lib.exception import AwsErrorException
from django.conf import settings
from ..models.database import Database

logger = logging.getLogger(__name__)


def get_all_databases():
    
    glue_client = boto3.client('glue')

    raw_db_list = []
    final_db_list = []

    try:
        logger.debug("getting list of databases from glue")
        resp = glue_client.get_databases()
        
        raw_db_list.extend(resp['DatabaseList'])


        while 'NextToken' in resp:
            logger.debug("getting additional databases from pagination")
            resp = glue_client.get_databases(NextToken=resp['NextToken'])
            raw_db_list.extend(resp['DatabaseList'])

    except ClientError as e:
        logger.error(f"error getting the list of databases from glue: {e}")
        raise AwsErrorException


    for raw_db in raw_db_list:

        logger.debug(f"processing db {raw_db['Name']}")

        final_db_list.append(Database(raw_db['Name'], raw_db['Description']))

    return final_db_list



