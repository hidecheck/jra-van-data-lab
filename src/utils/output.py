def show_one_line(df, sort_index=True):
    if sort_index:
        s = df.iloc[0].sort_index()
    else:
        s = df.iloc[0]

    for i, v in s.items():
        print(i, v)


def show_line(df, index=0, sort_index=True):
    if sort_index:
        s = df.iloc[index].sort_index()
    else:
        s = df.iloc[index]

    for i, v in s.items():
        print(i, v)


def show_series(series, sort_index=True):
    if sort_index:
        s = series.sort_index()
    else:
        s = series

    for i, v in s.items():
        print(i, v)

