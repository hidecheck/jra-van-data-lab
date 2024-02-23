EXCEPT_COLS = [
    "record_id",
    "data_sakusei_nengappi",
    "fukushoku_hyoji",
]

def show_columns():
    with open("db_spec_csv/馬毎レース情報ヘッダ.csv") as f:
        line = f.read()
    cols = line.split(",")
    for col in cols:
        if col in EXCEPT_COLS:
            print(f'    "{col}"     # 除外,')
        else:
            print(f'    "{col}",')


if __name__ == '__main__':
    show_columns()
