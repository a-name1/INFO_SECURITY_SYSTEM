"""
RSA非对称加密算法
使用PyCryptodome库实现
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class RSAKeyPair:
    """RSA密钥对管理"""
    
    def __init__(self, key_size: int = 2048):
        """
        生成RSA密钥对
        
        Args:
            key_size: 密钥大小（比特数，默认2048）
        """
        self.key = RSA.generate(key_size)
        self.public_key = self.key.publickey()
    
    def get_public_key_pem(self) -> str:
        """获取公钥（PEM格式）"""
        return self.public_key.export_key().decode()
    
    def get_private_key_pem(self) -> str:
        """获取私钥（PEM格式）"""
        return self.key.export_key().decode()


def encrypt(plaintext: str, public_key_pem: str) -> str:
    """
    RSA公钥加密
    
    Args:
        plaintext: 明文
        public_key_pem: 公钥（PEM格式）
    
    Returns:
        Base64编码的密文
    """
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()


def decrypt(ciphertext_b64: str, private_key_pem: str) -> str:
    """
    RSA私钥解密
    
    Args:
        ciphertext_b64: Base64编码的密文
        private_key_pem: 私钥（PEM格式）
    
    Returns:
        明文
    """
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()


def sign(message: str, private_key_pem: str) -> str:
    """
    RSA签名
    
    Args:
        message: 要签名的消息
        private_key_pem: 私钥（PEM格式）
    
    Returns:
        Base64编码的签名
    """
    from Crypto.Signature import pkcs1_v1_5
    from Crypto.Hash import SHA256
    
    private_key = RSA.import_key(private_key_pem)
    h = SHA256.new(message.encode())
    signature = pkcs1_v1_5.new(private_key).sign(h)
    return base64.b64encode(signature).decode()


def verify(message: str, signature_b64: str, public_key_pem: str) -> bool:
    """
    验证RSA签名
    
    Args:
        message: 原始消息
        signature_b64: Base64编码的签名
        public_key_pem: 公钥（PEM格式）
    
    Returns:
        签名是否有效
    """
    from Crypto.Signature import pkcs1_v1_5
    from Crypto.Hash import SHA256
    
    public_key = RSA.import_key(public_key_pem)
    h = SHA256.new(message.encode())
    signature = base64.b64decode(signature_b64)
    return pkcs1_v1_5.new(public_key).verify(h, signature)
