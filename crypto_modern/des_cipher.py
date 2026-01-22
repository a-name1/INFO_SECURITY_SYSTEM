"""
DES对称加密算法 (Data Encryption Standard)
使用PyCryptodome库实现
"""
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def _ensure_8_bytes(key: str) -> bytes:
    """确保密钥为8字节"""
    key_bytes = key.encode() if isinstance(key, str) else key
    if len(key_bytes) < 8:
        key_bytes = key_bytes.ljust(8, b'\0')
    elif len(key_bytes) > 8:
        key_bytes = key_bytes[:8]
    return key_bytes


def encrypt(plaintext: str, key: str) -> str:
    """
    DES加密
    
    Args:
        plaintext: 明文
        key: 密钥（会自动填充或截断到8字节）
    
    Returns:
        Base64编码的密文（包含IV）
    """
    key_bytes = _ensure_8_bytes(key)
    cipher = DES.new(key_bytes, DES.MODE_CBC)
    iv = cipher.iv
    
    plaintext_bytes = plaintext.encode()
    padded_plaintext = pad(plaintext_bytes, DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # 将IV和密文组合，然后Base64编码
    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode()


def decrypt(ciphertext_b64: str, key: str) -> str:
    """
    DES解密
    
    Args:
        ciphertext_b64: Base64编码的密文
        key: 密钥
    
    Returns:
        明文
    """
    key_bytes = _ensure_8_bytes(key)
    encrypted_data = base64.b64decode(ciphertext_b64)
    
    # 提取IV和密文
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    
    cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, DES.block_size)
    
    return plaintext.decode()
