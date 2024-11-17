"""
JRA_VAN 仕様:
  Table No: 3
  Table ID: jvd_se
  名称: 馬毎レース情報

本システム 仕様:
  名称: entry_hourse
"""
from const.table_columns import jvd_ra
from const.table_columns.jvd_ra import CUSTOM_COL_RACE_ID, CUSTOM_COL_RACE_GRADE

CUSTOM_COL_WEIGHT_DIFFERENCE = "_weight_diff"
CUSTOM_COL_WIN_BET = "_win_bet" # 単勝 (float)
CUSTOM_COL_WIN_FAVORITE = "_win_fav" # 単勝人気 (int)
CUSTOM_COL_GENDER = "_gender"
CUSTOM_COL_JOCKEY = "_jockey"

ALL_COLUMNS = [
    "record_id",    # 除外
    "data_kubun",
    "data_sakusei_nengappi",   # 除外
    "kaisai_nen",
    "kaisai_tsukihi",
    "keibajo_code",
    "kaisai_kai",
    "kaisai_nichime",
    "race_bango",
    "wakuban",
    "umaban",
    "ketto_toroku_bango",
    "bamei",
    "umakigo_code",
    "seibetsu_code",
    "hinshu_code",
    "moshoku_code",
    "barei",
    "tozai_shozoku_code",
    "chokyoshi_code",
    "chokyoshimei_ryakusho",
    "banushi_code",
    "banushimei",
    "fukushoku_hyoji",    # 除外 カンマ区切りの文字含む
    "yobi_1",
    "futan_juryo",
    "futan_juryo_henkomae",
    "blinker_shiyo_kubun",
    "yobi_2",
    "kishu_code",
    "kishu_code_henkomae",
    "kishumei_ryakusho",
    "kishumei_ryakusho_henkomae",
    "kishu_minarai_code",
    "kishu_minarai_code_henkomae",
    "bataiju",
    "zogen_fugo",
    "zogen_sa",
    "ijo_kubun_code",
    "nyusen_juni",
    "kakutei_chakujun",
    "dochaku_kubun",
    "dochaku_tosu",
    "soha_time",
    "chakusa_code_1",
    "chakusa_code_2",
    "chakusa_code_3",
    "corner_1",
    "corner_2",
    "corner_3",
    "corner_4",
    "tansho_odds",
    "tansho_ninkijun",
    "kakutoku_honshokin",
    "kakutoku_fukashokin",
    "yobi_3",
    "yobi_4",
    "kohan_4f",
    "kohan_3f",
    "aiteuma_joho_1",
    "aiteuma_joho_2",
    "aiteuma_joho_3",
    "time_sa",
    "record_koshin_kubun",
    "mining_kubun",
    "yoso_soha_time",
    "yoso_gosa_plus",
    "yoso_gosa_minus",
    "yoso_juni",
    "kyakushitsu_hantei",
]

MINIMUM_COLUMNS = [
    CUSTOM_COL_RACE_ID,     # [APPEND] レースID: YYYY-mm-dd_<競馬場コード>_<レースNo>
    "race_bango",
    "wakuban",
    "umaban",
    "bamei",
    CUSTOM_COL_GENDER,
    "barei",
    CUSTOM_COL_JOCKEY,     # [APPEND] 騎手略称のスペース除去
    "bataiju",
    CUSTOM_COL_WEIGHT_DIFFERENCE,   # 符号付き馬体重（文字列）
    "kakutei_chakujun",
    CUSTOM_COL_WIN_BET,
    CUSTOM_COL_WIN_FAVORITE,
]

ENTRY_HORSE_PROJECTIONS = [
    "data_kubun",
    "kaisai_nen",
    "kaisai_tsukihi",
    "keibajo_code",
    "kaisai_kai",
    "kaisai_nichime",
    "race_bango",
    "wakuban",
    "umaban",
    "ketto_toroku_bango",
    "bamei",
    "umakigo_code",
    "seibetsu_code",
    "hinshu_code",
    "moshoku_code",
    "barei",
    "tozai_shozoku_code",
    "chokyoshi_code",
    "chokyoshimei_ryakusho",
    "banushi_code",
    "banushimei",
    "yobi_1",
    "futan_juryo",
    "futan_juryo_henkomae",
    "blinker_shiyo_kubun",
    "yobi_2",
    "kishu_code",
    "kishu_code_henkomae",
    "kishumei_ryakusho",
    "kishumei_ryakusho_henkomae",
    "kishu_minarai_code",
    "kishu_minarai_code_henkomae",
    "bataiju",
    "zogen_fugo",
    "zogen_sa",
    "ijo_kubun_code",
    "nyusen_juni",
    "kakutei_chakujun",
    "dochaku_kubun",
    "dochaku_tosu",
    "soha_time",
    "chakusa_code_1",
    "chakusa_code_2",
    "chakusa_code_3",
    "corner_1",
    "corner_2",
    "corner_3",
    "corner_4",
    "tansho_odds",
    "tansho_ninkijun",
    "kakutoku_honshokin",
    "kakutoku_fukashokin",
    "yobi_3",
    "yobi_4",
    "kohan_4f",
    "kohan_3f",
    "aiteuma_joho_1",
    "aiteuma_joho_2",
    "aiteuma_joho_3",
    "time_sa",
    "record_koshin_kubun",
    "mining_kubun",
    "yoso_soha_time",
    "yoso_gosa_plus",
    "yoso_gosa_minus",
    "yoso_juni",
    "kyakushitsu_hantei",
]