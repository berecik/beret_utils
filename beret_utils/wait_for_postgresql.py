import psycopg2
import os
import time

NAME = os.environ.get('POSTGRES_DB', '../python_indicators')
USER = os.environ.get('POSTGRES_USER', 'postgres')
PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
HOST = os.environ.get('POSTGRES_HOST', 'localhost')
PORT = os.environ.get('POSTGRES_PORT', 5432)
RETRIES = os.environ.get('POSTGRES_RETRIES', 120)
WAIT = os.environ.get('POSTGRES_WAIT', 5)

for i in range(RETRIES):
    try:
        with psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=NAME
        ):
            print("PostgreSQL is ready for connection now!")
            break

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        print("Let wait {} seconds for postgresql connection {} time".format(WAIT, i+1))
        time.sleep(WAIT)

