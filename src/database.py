from urllib.parse import urlparse
import psycopg2
import os
from dotenv import load_dotenv

try:
    load_dotenv(os.path.join(os.getcwd(), '.env'))
except:
    pass

database = os.environ['DATABASE_URL']
table = os.environ['DATABASE_TABLE']

def connect():
    result = urlparse(database)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )

    return connection

def insert_images(data, columns=['idd', 'description', 'tags', 'users', 'path', 'date']):
    """
        data is a dictionary of column:val to insert into db
        columns is the columns in the db
        enforce python types casting to db type.
    """
    values = [data[i] if i in data else None for i in columns]
    cols = ','.join(columns)
    print(values)
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO """+table+""" ("""+cols+""") VALUES(%s, %s, %s, %s, %s, %s)""", values)
    connection.commit()
    cursor.close()
    connection.close()