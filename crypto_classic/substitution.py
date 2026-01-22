"""
单表置换密码 (Simple Substitution Cipher)
使用替换表进行加密
"""

def encrypt(plaintext: str, key: str = None) -> str:
    """
    单表置换加密
    
    Args:
        plaintext: 明文
        key: 26字母的替换表（默认为None，使用默认替换表）
    
    Returns:
        密文
    """
    if key is None:
        # 默认替换表（可以自定义）
        key = "qwertyuiopasdfghjklzxcvbnm"
    
    if len(key) != 26:
        raise ValueError("替换表必须包含26个不同的字母")
    
    # 验证替换表中没有重复字母
    if len(set(key.lower())) != 26:
        raise ValueError("替换表中不能有重复的字母")
    
    ciphertext = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    for char in plaintext:
        if char.lower() in alphabet:
            # 找到字母在标准字母表中的位置
            index = alphabet.index(char.lower())
            # 使用替换表中对应位置的字母
            substituted = key[index]
            # 保持大小写
            if char.isupper():
                substituted = substituted.upper()
            ciphertext.append(substituted)
        else:
            # 非字母字符保持不变
            ciphertext.append(char)
    
    return ''.join(ciphertext)


def decrypt(ciphertext: str, key: str = None) -> str:
    """
    单表置换解密
    
    Args:
        ciphertext: 密文
        key: 26字母的替换表（默认为None，使用默认替换表）
    
    Returns:
        明文
    """
    if key is None:
        key = "qwertyuiopasdfghjklzxcvbnm"
    
    if len(key) != 26:
        raise ValueError("替换表必须包含26个不同的字母")
    
    # 创建逆向映射：密文字母 -> 明文字母
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    reverse_key = {}
    for i, char in enumerate(key.lower()):
        reverse_key[char] = alphabet[i]
    
    plaintext = []
    
    for char in ciphertext:
        if char.lower() in reverse_key:
            decrypted = reverse_key[char.lower()]
            if char.isupper():
                decrypted = decrypted.upper()
            plaintext.append(decrypted)
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)


def generate_key() -> str:
    """
    生成随机替换表
    
    Returns:
        随机生成的26字母替换表
    """
    import random
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    random.shuffle(alphabet)
    return ''.join(alphabet)
