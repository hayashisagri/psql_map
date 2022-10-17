## 訪問した都道府県の記録アプリ

## サービス説明
[スライド](https://docs.google.com/presentation/d/1yJjjX5R6KVSWG3Itg-NjYuK9IoXtMCh2H46ZAtJCJvk/edit?usp=sharing)

## サービスの起動方法
1. ```git clone git@github.com:hayashisagri/psql_map.git```
2. move to project root
3. ```docker-compose up```
4. ```python manage.py migrate```
5. ```python manage.py createsuperuser```
6. access to localhost http://0.0.0.0:8000/home/