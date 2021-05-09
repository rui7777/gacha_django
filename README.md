# Django REST Frameworkでガチャを実装する

## 概要

Django REST Frameworkを用いて以下のAPIを実装した。

- ユーザー作成
- ログイン
- ガチャのためのアイテム作成
- ガチャ

目標 : Djangoの基本的な概念にのっとり期待通りに動作するREST APIを作成する

## 開発環境

- PC
    - OS : macOS Big Sur 11.2.3
    - CPU : Intel Core i5
    - Memory : 16GB
- 言語
    - Python : 3.9.0
    - JavaScript
- フレームワーク
    - Django : 3.2
    - Django REST Framework : 3.12.4
    - Vue : 2.6.12
- データベース
    - SQLite3

## セットアップ手順メモ(一から)

```
$ mkdir gacha_django
$ cd gacha_django
$ pip install django
$ pip install djangorestframework
$ django-admin startproject config .
$ python manage.py startapp accounts
$ python manage.py startapp apiv1
$ python manage.py startapp gacha
```

ここまでできたらコードを書き始める。 動作確認を行う時には以下のコマンドを入力する。

```
$ python manage.py makemigrations accounts
$ python manage.py makemigrations gacha
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

http://127.0.0.1:8000 にアクセスして動作を確認する。

## 設計指針

- 全ての画面共通
    - 検証しやすくするためにVue.jsを用いて各画面のフォームを作成する
    - 認証にはCookie認証を用いる

- ユーザー認証まわり
    - ユーザー名、メールアドレス、パスワードは必須項目
    - ログインにはメールアドレスとパスワードを用いる

- ガチャ
    - ユーザーがログイン状態でないと操作できない
    - スーパーユーザーのみガチャのアイテムを登録できる
    - ガチャを回す際は通常ガチャ、11連ガチャ(SR以上確定)、11連ガチャ(SSR確定)のいずれかを選択する。各アイテムの重みに従い、アイテム名とレア度が出力される

### データ構造

- ユーザー

```
{
  username : Char(max_length=30)
  first_name : Char(max_length=30, blank=True)
  last_name : Char(max_length=30, blank=True)
  email : Email(max_length=255)
  profile : Char(max_length=255)
  is_active : Bool
  is_staff : Bool
  is_admin : Bool
  date_joined : DateTime
}
```

- ガチャ(アイテム)

```
{ 
  id : UUID
  name : Char(max_length=20)
  weight : Int
  rarity : Char(choices=["SSR", "SR", "R"])
  created_at : DateTime
}
```

## 動作確認

### ユーザー登録

- リクエスト

```
$ curl -X POST -H "Content-Type: application/json" -d \
  '{ 
     "username" : "TestUser", 
     "email" : "test@test.com", 
     "profile" : "Hello, test!", 
     "password" : "pass12345" 
  }' http://127.0.0.1:8000/api/register/
```

- レスポンス

```
{
  "id":5,
  "username":"TestUser",
  "email":"test@test.com",
  "profile":"Hello, test!"
}
```

### ログイン

- リクエスト

```
$ curl -X POST -b "sessionid=...;csrftoken=..." -H \ 
  "Content-Type:application/json" -H "X-CSRFToken:..." -d \
  '{ 
     "email" : "test@test.com"
     "password" : "pass12345"
  }' http://127.0.0.1:8000/api-auth/login/
```

### ガチャアイテム追加

- リクエスト

```
$ curl -X POST -b "sessionid=...;csrftoken=..." -H \ 
  "Content-Type:application/json" -H "X-CSRFToken:..." -d \
  '{ 
     "name" : "ITEM0"
     "weight" : 3
     "rarity" : "SSR"
  }' http://127.0.0.1:8000/api/v1/register/
```

- レスポンス

```
{ 
  "name" : "ITEM0"
  "weight" : 3
  "rarity" : "SSR"
}
```

### ガチャを回す

- リクエスト

```
$ curl -X POST -b "sessionid=...;csrftoken=..." -H \ 
  "Content-Type:application/json" -H "X-CSRFToken:..." -d \
  '{ 
     "choice" : "通常ガチャ" 
  }' http://127.0.0.1:8000/api/v1/result/
```

- レスポンス

```
{
  "result": [
    {
      "name": "ITEM8",
      "rarity": "R"
    }
  ]
}
```

## 所感

Djangoはフルスタックフレームワークということもあり、管理画面やAPIの動作確認画面が自動的に生成されるため、非常に扱いやすく便利だと感じた。  
また、モデル、シリアライザ、ビューと役割ごとに処理が明確に分けられているため、チームで開発するとなると使いやすいだろうなと感じた。

一方でガチャのようなモデルに従わない入出力(リクエスト: ガチャの種類, レスポンス: ガチャのアイテムがランダムに返される)の場合は急に難易度が上がる気がした。  
どういうことかというと、モデルに従ったシリアライザやビューは少ないコードで簡潔に書くことができる(そういったテンプレートが用意されている)が、そうでない時は自分で関数をカスタマイズしてほとんど一からコードを書く必要がある。  
そういった観点からユーザー登録やログインは比較的簡単に実装することができたが、ガチャを実装するとなるとかなり苦労した。

## 残課題

- オーブ(ガチャを回すためのアイテムをオーブと呼称することにする)の実装(現在は無限に回せる)
- テストコードの実装と検証

## 参考サイト

### Django全般

- https://qiita.com/kimihiro_n/items/86e0a9e619720e57ecd8
- (書籍) 横瀬 明仁. 現場で使える Django REST Framework の教科書 （Django の教科書シリーズ

### ユーザー認証まわり

- https://di-acc2.com/programming/python/2534/
- https://qiita.com/xKxAxKx/items/60e8fb93d6bbeebcf065

### ガチャ関連

- https://qiita.com/ynakayama/items/536de2f575086685f1de