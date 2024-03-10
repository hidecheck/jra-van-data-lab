# jra-van-data-lab

## DB 仕様メモ
- 共通テーブル名
  - JRA-VANデータラボのテーブル名: `"jvd_<レコード種別ID>`
  - 地方競馬DATAのテーブル名: `nvd_<レコード種別ID>`
- 共通列名
  - 全てのテーブルに必ず存在する列名  
  - record_id
    - 論理名: レコード種別ID
    - JRA-VAN のデータ識別子的なもの
    - 例
      - RA: レース詳細
      - SE: 馬毎レース情報
- 馬毎情報
  - 馬体重
    - 単位:kg
    - 002Kg～998Kgまでが有効値
    - 999:今走計量不能
    - 000:出走取消
    - '   ': 初期値（スペース３つ）
  - 後3ハロン
    - 999: 出走取消・競走除外・発走除外・競走中止・タイムオーバー
    - 000: 初期値
    - ※ 過去分のデータは後4ハロンが設定されているものもある(その場合は後3ハロンが初期値

## コラム
- [データマイニング予測の仕組み
](https://jra-van.jp/fun/dm/mining.html)