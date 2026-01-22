"""
AES对称加密算法 (Advanced Encryption Standard)
使用PyCryptodome库实现，支持256位密钥
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def _ensure_key_length(key: str, key_size: int = 32) -> bytes:
    """确保密钥为指定长度（32字节=256位）"""
    key_bytes = key.encode() if isinstance(key, str) else key
    if len(key_bytes) < key_size:
        key_bytes = key_bytes.ljust(key_size, b'\0')
    elif len(key_bytes) > key_size:
        key_bytes = key_bytes[:key_size]
    return key_bytes


def encrypt(plaintext: str, key: str, key_size: int = 32) -> str:
    """
    AES加密
    
    Args:
        plaintext: 明文
        key: 密钥（会自动填充或截断到指定长度）
        key_size: 密钥大小（16、24或32字节，默认32）
    
    Returns:
        Base64编码的密文（包含IV）
    """
    key_bytes = _ensure_key_length(key, key_size)
    plaintext_bytes = plaintext.encode()
    
    # 使用CBC模式
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    iv = cipher.iv
    
    padded_plaintext = pad(plaintext_bytes, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # 将IV和密文组合，然后Base64编码
    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode()


def decrypt(ciphertext_b64: str, key: str, key_size: int = 32) -> str:
    """
    AES解密
    
    Args:
        ciphertext_b64: Base64编码的密文
        key: 密钥
        key_size: 密钥大小（默认32）
    
    Returns:
        明文
    """
    key_bytes = _ensure_key_length(key, key_size)
    encrypted_data = base64.b64decode(ciphertext_b64)
    
    # 提取IV和密文
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    
    return plaintext.decode()
