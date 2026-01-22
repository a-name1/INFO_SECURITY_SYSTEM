"""
MD5哈希算法
用于信息摘要和密码哈希
"""
import hashlib


def hash_text(text: str) -> str:
    """
    计算文本的MD5哈希值
    
    Args:
        text: 要哈希的文本
    
    Returns:
        MD5哈希值（十六进制字符串）
    """
    return hashlib.md5(text.encode()).hexdigest()


def hash_bytes(data: bytes) -> str:
    """
    计算二进制数据的MD5哈希值
    
    Args:
        data: 要哈希的二进制数据
    
    Returns:
        MD5哈希值（十六进制字符串）
    """
    return hashlib.md5(data).hexdigest()


def hash_file(filepath: str) -> str:
    """
    计算文件的MD5哈希值
    
    Args:
        filepath: 文件路径
    
    Returns:
        MD5哈希值（十六进制字符串）
    """
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()
