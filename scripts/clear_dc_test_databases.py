#!/usr/bin/python
import boto3

def clear_databases(number_of_dbs):

    glue_client = boto3.client('glue')

    for db in range(number_of_dbs):

        print(f"deleting database {db}")

        db_name = f"test-database-{db}"

        resp = glue_client.delete_database(
                Name=db_name
            )

## Main ##

num_dbs = 4

print("deleting test databases")
clear_databases(num_dbs)

