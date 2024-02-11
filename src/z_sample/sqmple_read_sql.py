import pandas as pd
import psycopg2
from sqlalchemy import create_engine

import config
from config import connection_config


def connect_with_psycopg2():
    sql = 'SELECT * FROM jvd_um;'
    connection = psycopg2.connect(**connection_config)
    df = pd.read_sql(sql=sql, con=connection)
    print(df.head())
    connection.close()


def connect_with_sqlalchemy():
    sql = 'SELECT * FROM jvd_um;'
    engine = create_engine(config.CREATE_ENGINE_URL)
    df = pd.read_sql(sql=sql, con=engine)
    print(df.head())
    engine.dispose()


def main():
    # connect_with_psycopg2()
    connect_with_sqlalchemy()


if __name__ == '__main__':
    main()
