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

## ZI データ
- CSV の取得方法: http://target.a.la9.jp/download/downloadzi.htm
- CSV のフォーマット
  - ファイル名: ZIYYmmDD.CSV ex) ZI240310.CSV
  - フォーマット: レースID, ZI指数01, ZI指数02, ...
  - レースID: <競馬場コード><YY年><N回><N日><レース番号> 
    - [JRA_VAN仕様](https://targetfaq.jra-van.jp/faq/detail?site=SVKNEGBV&category=47&id=658#:~:text=%E7%AB%B6%E8%B5%B0%E8%AD%98%E5%88%A5%E3%82%B3%E3%83%BC%E3%83%89(%E3%83%AC%E3%83%BC%E3%82%B9ID)&text=%E3%81%93%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AF%E3%80%81JRA%2DVAN,%E3%81%A8%E5%91%BC%E3%81%B6%E3%81%93%E3%81%A8%E3%82%82%E3%81%82%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82)
    - 旧レースIDが採用されている
    - ex) 2024年 中山第2回6日目1レースの場合 `06242601`
## コラム
- [データマイニング予測の仕組み](https://jra-van.jp/fun/dm/mining.html)