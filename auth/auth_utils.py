"""
身份认证模块 - 工具函数
提供密码加密、验证等功能
"""
import hashlib
import secrets

def hash_password(password: str) -> str:
    """
    使用MD5算法对密码进行哈希处理
    
    Args:
        password: 明文密码
    
    Returns:
        哈希后的密码
    """
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    验证密码是否与哈希值匹配
    
    Args:
        password: 明文密码
        password_hash: 存储的哈希值
    
    Returns:
        是否匹配
    """
    return hash_password(password) == password_hash


def generate_token(length: int = 32) -> str:
    """
    生成安全的随机令牌
    
    Args:
        length: 令牌长度
    
    Returns:
        随机令牌
    """
    return secrets.token_hex(length // 2)
