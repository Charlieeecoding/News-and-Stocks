import requests
import psycopg2 as pg
import os
import json
import logging

log = logging.getLogger(__name__)

# connecting to Postgres database and save data
def connect_to_postgres():
    print("Connecting to PostgreSQL database...")
    try:
        connection = pg.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )

        print("Connection successful.")
        return connection
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None, None


def table_creation(table_name, columns_definition):
    connection = connect_to_postgres()
    if connection is None:
        print("Failed to connect to the database. Table creation aborted.")
        return

    cursor = connection.cursor()
    try:
        create_table_query = 
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table {table_name} created successfully.")
    except Exception as error:
        print(f"Error creating table {table_name}: {error}")
    finally:
        cursor.close()
        connection.close()


def ingest_data_to_postgres(data, table_name):
    connection = connect_to_postgres()
    if connection is None:
        print("Failed to connect to the database. Data ingestion aborted.")
        return

    cursor = connection.cursor()
    try:
        for item in data:
            # Assuming 'item' is a dictionary and table has columns matching the keys
            columns = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(insert_query, list(item.values()))

        connection.commit()
        print(f"Data ingested successfully into {table_name}.")
    except Exception as error:
        print(f"Error ingesting data into PostgreSQL: {error}")
    finally:
        cursor.close()
        connection.close()