"""
JRA_VAN 仕様:
  Table No: 2
  Table ID: jvd_ra
  名称: レース詳細

本システム 仕様:
  名称: race
"""

ALL_COLUMNS = [
    "record_id",
    "data_kubun",
    "data_sakusei_nengappi",
    "kaisai_nen",
    "kaisai_tsukihi",
    "keibajo_code",
    "kaisai_kai",
    "kaisai_nichime",
    "race_bango",
    "yobi_code",
    "tokubetsu_kyoso_bango",
    "kyosomei_hondai",
    "kyosomei_fukudai",
    "kyosomei_kakkonai",
    "kyosomei_hondai_eur",
    "kyosomei_fukudai_eur",
    "kyosomei_kakkonai_eur",
    "kyosomei_ryakusho_10",
    "kyosomei_ryakusho_6",
    "kyosomei_ryakusho_3",
    "kyosomei_kubun",
    "jusho_kaiji",
    "grade_code",
    "grade_code_henkomae",
    "kyoso_shubetsu_code",
    "kyoso_kigo_code",
    "juryo_shubetsu_code",
    "kyoso_joken_code_2sai",
    "kyoso_joken_code_3sai",
    "kyoso_joken_code_4sai",
    "kyoso_joken_code_5sai_ijo",
    "kyoso_joken_code",
    "kyoso_joken_meisho",
    "kyori",
    "kyori_henkomae",
    "track_code",
    "track_code_henkomae",
    "course_kubun",
    "course_kubun_henkomae",
    "honshokin",
    "honshokin_henkomae",
    "fukashokin",
    "fukashokin_henkomae",
    "hasso_jikoku",
    "hasso_jikoku_henkomae",
    "toroku_tosu",
    "shusso_tosu",
    "nyusen_tosu",
    "tenko_code",
    "babajotai_code_shiba",
    "babajotai_code_dirt",
    "lap_time",
    "shogai_mile_time",
    "zenhan_3f",
    "zenhan_4f",
    "kohan_3f",
    "kohan_4f",
    "corner_tsuka_juni_1",
    "corner_tsuka_juni_2",
    "corner_tsuka_juni_3",
    "corner_tsuka_juni_4",
    "record_koshin_kubun",
]

# fmt: off
TYPICAL_COLUMNS = [
    "race_id",            # [APPEND] レースID: YYYY-mm-dd_<競馬場コード>_<レースNo>
    "race_name",          # [APPEND] レース名
    "kaisai_nen",
    "kaisai_tsukihi",
    "keibajo_code",
    "kaisai_kai",
    "kaisai_nichime",
    "race_bango",
    "kyosomei_hondai",
    "kyosomei_fukudai",
    "kyosomei_kakkonai",
    "jusho_kaiji",          # 第 N 回
    "grade_code",           # <コード表 2003.グレードコード>参照
    "kyoso_shubetsu_code",  # <コード表 2005.競走種別コード>参照
    "kyoso_kigo_code",      # <コード表 2006.競走記号コード>参照 例) 牝, 混合）,（国際）
    "juryo_shubetsu_code",  # <コード表 2008.重量種別コード>参照
    "kyoso_joken_code_2sai",      # 2歳馬の競走条件   <コード表 2007.競走条件コード>参照
    "kyoso_joken_code_3sai",      # 3歳馬の競走条件   <コード表 2007.競走条件コード>参照
    "kyoso_joken_code_4sai",      # 4歳馬の競走条件   <コード表 2007.競走条件コード>参照
    "kyoso_joken_code_5sai_ijo",  # 5歳以上馬の競走条件   <コード表 2007.競走条件コード>参照
    "kyoso_joken_code",           # 出走可能な最も馬齢が若い馬に対する条件   <コード表 2007.競走条件コード>参照
    "kyori",
    "track_code",                 # <コード表 2009.トラックコード>参照 例) 芝・左, ダート・右
    "course_kubun",               # 半角2文字 使用するコースを設定, "A " ~ "E " を設定
    "toroku_tosu",
    "shusso_tosu",
    "tenko_code",                 # <コード表 2011.天候コード>参照
    "babajotai_code_shiba",       # <コード表 2010.馬場状態コード>参照
    "babajotai_code_dirt",        # <コード表 2010.馬場状態コード>参照
    "zenhan_3f",
    "zenhan_4f",
    "kohan_3f",
    "kohan_4f",
    "record_koshin_kubun",        # 0:初期値 1:基準タイムとなったレース 2:コースレコードを更新したレース
]

MINIMUM_COLUMNS = [
    "race_id",            # [APPEND] レースID: YYYY-mm-dd_<競馬場コード>_<レースNo>
    "race_name",          # [APPEND] レース名
    "race_grade",         # [APPEND] 条件、グレードなど
    "race_bango",
    "kyosomei_hondai",
    "jusho_kaiji",        # 第 N 回
    "kyori",
    "track_code",         # <コード表 2009.トラックコード>参照 例) 芝・左, ダート・右
    "toroku_tosu",
]
# fmt: on
