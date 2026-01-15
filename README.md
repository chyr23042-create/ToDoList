# ToDoリスト管理アプリ

## 概要
本アプリケーションは、タスクを管理するための  
**データベースを用いた Web アプリケーション**である。

Flask と SQLite を用いて、タスクの追加・表示・更新・削除を行うことができる。  
タスク情報はデータベースに保存されるため、アプリケーションを終了・再起動しても
内容は保持される。

---

## 使用技術
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML / CSS（Jinja2 テンプレート）

---

## ディレクトリ構成

```text
.
├─ app.py                
├─ templates/            
│  └─ index.html
├─ requirements.txt      
└─ README.md             
```

## 実行方法

### 1. 必要なライブラリをインストール
```bash
pip install -r requirements.txt

```

### アプリケーションを起動
```bash
python app.py

```
### ブラウザにアクセス
アプリケーション起動後、ローカル環境にてブラウザで  
`http://127.0.0.1:5000/` にアクセスすることでアプリを利用できる。
