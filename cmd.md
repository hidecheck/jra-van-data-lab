* Docker compose 起動
  * `docker-compose up -d`
* Docker compose 終了
  * `docker-compose down`
* postgreSQL 接続
  * `psql -h localhost -U postgres -d pckeiba`
* リストア
  * `cat pckeiba.sql | docker exec -i my_postgres psql -U postgres -d pckeiba`
