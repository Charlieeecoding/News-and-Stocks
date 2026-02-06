import psycopg2 as pg
import os
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# connecting to Postgres database and save data
def connect_to_postgres():
    log.info("Connecting to PostgreSQL database...")
    try:
        connection = pg.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB')
        )

        log.info("Connection successful.")
        
        return connection
    
    except Exception as error:
        log.info(f"Error connecting to PostgreSQL database: {error}")
        
        return None, None


def table_name_list(folder_path):
    log.info(f"Extracting table name list for table creation: {folder_path}")

    try:
        all_table_names = []
        file_paths = Path(folder_path)
        
        files = [entry.name for entry in file_paths.iterdir() if entry.is_file()]

        return files
    
    except Exception as error:
        log.info(f"Error extracting table names from folder {folder_path}: {error}")
        
        return all_table_names


def table_creation(table_name, table_creation_query):
    connection = connect_to_postgres()
    if connection is None:
        log.info("Failed to connect to the database. Table creation aborted.")
        return

    cursor = connection.cursor()
    try:
        log.info(f"Creating table {table_name}")
        
        with open(table_creation_query, 'r') as f:
            creation_sql_script = f.read()

        cursor.execute(creation_sql_script)

        connection.commit()
        log.info(f"Table {table_name} created successfully.")
    except Exception as error:
        log.info(f"Error creating table {table_name}: {error}")
    finally:
        cursor.close()
        connection.close()


def ingest_data_to_postgres(data, table_name):
    connection = connect_to_postgres()
    
    if connection is None:
        log.info("Failed to connect to the database. Data ingestion aborted.")
        
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
        
        log.info(f"Data ingested successfully into {table_name}.")
    
    except Exception as error:
        log.info(f"Error ingesting data into PostgreSQL: {error}")
    
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    connection_test = connect_to_postgres()
    
    if connection_test:
        log.info("PostgreSQL connection test successful.")
        connection_test.close()
    
    table_name_list("NEWS-AND-STOCKS/postgre/")

    sql_file = os.path.join(os.getcwd(), "./postgre/news_bronze.sql")
    table_creation('news_data', sql_file)