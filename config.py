"""
全局配置文件
"""
import os

# Flask应用配置
SECRET_KEY = 'your-secret-key-change-in-production'
DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///./database/users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200MB

# 图像分存配置
SHAMIR_THRESHOLD = 3  # Shamir方案的阈值
SHAMIR_SHARES = 5     # 生成的分片数量

# 密钥配置
RSA_KEY_SIZE = 2048
AES_KEY_SIZE = 32  # 256-bit

# 创建必要的文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(SQLALCHEMY_DATABASE_URI.split('///')[1]), exist_ok=True)
