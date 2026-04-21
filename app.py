import os
from flask import Flask
from app.routes import register_blueprints

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 設定 Secret Key，開發環境給個預設值以防沒有 env
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_12345')

    # 註冊所有藍圖路由
    register_blueprints(app)

    return app

def init_db():
    from app.models.transaction import get_db_connection
    import sqlite3
    import os

    db_path = 'instance/database.db'
    schema_path = 'database/schema.sql'

    # 若 database 資料夾不存在（防呆），雖然 schema 本身不需要
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} does not exist.")
        return

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn = get_db_connection()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
