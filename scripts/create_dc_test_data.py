#!/usr/bin/python
import boto3
import random

col_types = [
    'byte',
    'short',
    'integer',
    'long',
    'float',
    'double',
    'decimal',
    'string',
    'boolean',
    'timestamp',
    'date'
]

def create_databases(number_of_dbs):

    glue_client = boto3.client('glue')

    for db in range(number_of_dbs):
        
        if db % 2:
            db_description = f"test description for db {db}"
        else:
            db_description = ""

        db_name = f"test-database-{db}"

        print(f"creating test database {db}")

        resp = glue_client.create_database(
                DatabaseInput={
                    'Name': db_name,
                    'Description': db_description,
                }
            )

def create_tables(number_of_dbs):

    glue_client = boto3.client('glue')

    for db in range(number_of_dbs):

        number_of_tables = random.randint(2, 400)

        db_name = f"test-database-{db}"

        print(f"creating {number_of_tables} for test database {db}")

        for table in range(number_of_tables):

            if table % 2:
                table_description = f"test description for table {table}"
            else:
                table_description = ""
            
            table_name = f"test-table-{table}"

            table_cols = []

            number_of_cols = random.randint(2, 100)

            for col in range(number_of_cols):

                if col % 2:
                    col_comment = f"random comment for column {col}"
                else:
                    col_comment = ""

                col_type = col_types[random.randint(0, 10)]
                col_name = f"test_column_{col}"

                column = {
                    "Name": col_name,
                    "Type": col_type,
                    "Comment": col_comment
                }

                table_cols.append(column)

            resp = glue_client.create_table(
                    DatabaseName=db_name,
                    TableInput={
                        'Name': table_name,
                        'Description': table_description,
                        'StorageDescriptor': {
                            'Columns': table_cols
                        }
                    }
                )


## Main ##

num_dbs = 4

print("creating test databases")
create_databases(num_dbs)


print("")
print("==================================")
print("")


print("creating tables for the databases")
create_tables(num_dbs)
