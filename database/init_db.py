"""
数据库初始化脚本
创建用户认证表
"""
import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_database():
    """初始化数据库，创建用户表"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"数据库初始化完成！数据库位置：{DATABASE_PATH}")

if __name__ == '__main__':
    init_database()
