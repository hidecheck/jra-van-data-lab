import pandas as pd
from sqlalchemy import create_engine

USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
DATABASE = 'pckeiba'
CREATE_ENGINE_URL = (f"postgresql://{USER}:{PASSWORD}@localhost:5432/{DATABASE}")


def get_mining_df():
    # サンプルデータ
    df = pd.DataFrame({
        "race_no": ["01", "02", "03"],
        "data1": ["010716", "010677", "010500"],
        "data2": ["020399", "020388", ""]
    })
    print(df)
    return df


def transform(df: pd.DataFrame):
    df["data1"] = df["data1"].str[2:]
    df["data2"] = df["data2"].str[2:]
    print(df)


def read_sql(engine):
    pass


def main():
    engine = create_engine(CREATE_ENGINE_URL)
    # read_sql(engine)
    df = get_mining_df()
    transform(df)

    engine.dispose()


if __name__ == '__main__':
    main()