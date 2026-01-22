"""
身份认证模块 - 路由
处理用户登录、注册等请求
"""
import sqlite3
from flask import Blueprint, request, jsonify, session, redirect, url_for
from auth.auth_utils import hash_password, verify_password
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../database/users.db')


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    请求体：
    {
        "username": "用户名",
        "password": "密码",
        "email": "邮箱（可选）"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        
        # 验证输入
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': '密码长度至少为6位'}), 400
        
        # 对密码进行MD5哈希
        password_hash = hash_password(password)
        
        # 保存到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                (username, password_hash, email or None)
            )
            conn.commit()
            return jsonify({'success': True, 'message': '注册成功！'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        finally:
            conn.close()
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    请求体：
    {
        "username": "用户名",
        "password": "密码"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
        
        # 查询用户
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
        
        # 验证密码
        if not verify_password(password, user['password_hash']):
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
        
        # 设置会话
        session['user_id'] = user['id']
        session['username'] = user['username']
        
        return jsonify({'success': True, 'message': '登录成功！'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'登录失败: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'success': True, 'message': '登出成功！'}), 200


@auth_bp.route('/check', methods=['GET'])
def check_login():
    """检查用户是否已登录"""
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'username': session.get('username')}), 200
    return jsonify({'logged_in': False}), 200
