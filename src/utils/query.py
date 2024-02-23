def get_jra_course_sql_where():
    """
    JRA の競馬場コードを取得する SQL WHERE 句を返す
    Returns
    -------

    """
    return "keibajo_code IN ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10')"


def set_jra_course_conditions_string(conditions_string):
    where = get_jra_course_sql_where()

    if not conditions_string:
        conditions_string = where
    else:
        conditions_string = f"{conditions_string} AND {where}"

    return conditions_string
