from urllib.parse import urlparse
import psycopg2
import os

path = os.environ['DATABASE_URL']
result = urlparse(path)

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

def insert_images(idd, description, tags, url, date, table='images'):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO """+table+""" (idd, description, tags, url, date) VALUES(%s, %s, %s, %s, %s)""", (idd, description, tags, url, date))
    connection.commit()
    cursor.close()