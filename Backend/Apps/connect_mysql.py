from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


# 连接数据库
def connect_db():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db = SQLAlchemy(app)
    return app, db


# 获取表结构并打印
def get_tables_info(app, db):
    with app.app_context():  # 进入 app 上下文
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        result = []
        for table in tables:
            columns = inspector.get_columns(table)
            col_info = [f"{col['name']} ({col['type']})" for col in columns]
            result.append(f"{table}: {', '.join(col_info)}")

        for line in result:
            print(line)


# ✅ 主程序入口
if __name__ == '__main__':
    app, db = connect_db()
    get_tables_info(app, db)
