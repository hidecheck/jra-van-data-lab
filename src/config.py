USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
DATABASE = 'pckeiba'
CREATE_ENGINE_URL = (f"postgresql://{USER}:{PASSWORD}@localhost:5432/{DATABASE}")

connection_config = {
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'database': DATABASE
}

