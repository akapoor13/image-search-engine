from urllib.parse import urlparse
import psycopg2
import os
from dotenv import load_dotenv
import src.constants as const
import pandas as pd
from src.nlp import similarity
from src.cv import image_matches
from src.upload import download_image_from_upload

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
    db = result.path[1:]
    hostname = result.hostname
    connection = psycopg2.connect(database=db,
                                  user=username,
                                  password=password,
                                  host=hostname)

    return connection


def insert_images(data, columns=const.DBCOLS_, db_table=table):
    """
        data is a dictionary of column:val to insert into db
        columns is the columns in the db
        enforce python types casting to db type.
    """
    values = [data[i] if i in data else None for i in columns]
    cols = ','.join(columns)

    # connect to db
    connection = connect()
    cursor = connection.cursor()

    # insert data
    cursor.execute(
        f"""INSERT INTO {db_table} ({cols}) """ +
        """ VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", values)

    # close connection
    connection.commit()
    cursor.close()
    connection.close()


def data_to_df(rows):
    data = [{col: val for col, val in zip(const.DBCOLS_, r)} for r in rows]
    df = pd.DataFrame(data)

    return df


def pull_db_data():
    # connect to db
    connection = connect()
    cursor = connection.cursor()

    # pull data
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    df = data_to_df(rows)

    # close connection
    connection.commit()
    cursor.close()
    connection.close()

    return df


def __format_list_of_ids(loi):
    return ','.join(map(lambda x: f"'{x}'", loi))


def query_picture_idd(list_of_idds):
    idds = __format_list_of_ids(list_of_idds)
    query_sql = f"""SELECT *
FROM {table}
WHERE idd in ({idds});"""

    # connect to db
    connection = connect()
    cursor = connection.cursor()

    # pull data
    cursor.execute(query_sql)
    rows = cursor.fetchall()
    df = data_to_df(rows)

    # close connection
    connection.commit()
    cursor.close()
    connection.close()

    return df


def update_image(data, key, columns=const.DBCOLS_):
    """
        data is a dictionary of column names and values to update
        key is a dictionary of column names and values to update on
    """
    where_key = []
    update_cols = []
    order_tuple = []

    for i in data:
        if i in const.DBCOLS_:
            update_cols.append(f'{i} = %s')
            order_tuple.append(i)

    for i in key:
        if i in const.DBCOLS_:
            where_key.append(f'{i} = %s')
            order_tuple.append(i)

    update_cols = ', '.join(update_cols)
    where_key = 'AND'.join(where_key)

    update_sql = f"""UPDATE {table}
SET {update_cols}
WHERE {where_key}"""

    # connect to db
    connection = connect()
    cursor = connection.cursor()

    # update data
    cursor.execute(update_sql,
                   [data[i] if i in data else key[i] for i in order_tuple])

    # close connection
    connection.commit()
    cursor.close()
    connection.close()


def query(query_type, query_input):
    if not query_input:
        df = pd.DataFrame(columns=const.DBCOLS_)

    elif query_type == const.DESINPUT_:
        df = pull_db_data()

        if not df.empty:
            df = similarity(df, query_input)

    elif query_type == const.UPLOADINPUT_:
        df = pull_db_data()
        path = download_image_from_upload('target', query_input)
        df = image_matches(df, path)

    elif query_type == const.IDINPUT_:
        df = query_picture_idd([query_input])
        df[const.SIMILARCOL_] = None

    return df


def remove_record(list_of_id, db_table=table):
    # formal delete query
    idds = __format_list_of_ids(list_of_id)
    delete_sql = f"""DELETE FROM {db_table} WHERE idd in ({idds});"""

    # connect to db
    connection = connect()
    cursor = connection.cursor()

    # delete ids
    cursor.execute(delete_sql)

    # close connection
    connection.commit()
    cursor.close()
    connection.close()
