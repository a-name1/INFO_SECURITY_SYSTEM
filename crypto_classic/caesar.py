"""
凯撒密码 (Caesar Cipher)
一种简单的置换密码
"""

def encrypt(plaintext: str, shift: int = 3) -> str:
    """
    凯撒加密
    
    Args:
        plaintext: 明文
        shift: 位移量（默认3）
    
    Returns:
        密文
    """
    ciphertext = []
    shift = shift % 26
    
    for char in plaintext:
        if char.isalpha():
            # 确定字符的范围（大写或小写）
            if char.isupper():
                # 大写字母
                shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # 小写字母
                shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(shifted)
        else:
            # 非字母字符保持不变
            ciphertext.append(char)
    
    return ''.join(ciphertext)


def decrypt(ciphertext: str, shift: int = 3) -> str:
    """
    凯撒解密
    
    Args:
        ciphertext: 密文
        shift: 位移量（默认3）
    
    Returns:
        明文
    """
    # 解密就是反向位移
    return encrypt(ciphertext, -shift)


def brute_force_crack(ciphertext: str) -> dict:
    """
    暴力破解凯撒密码（尝试所有可能的位移）
    
    Args:
        ciphertext: 密文
    
    Returns:
        包含所有可能的明文的字典 {shift: plaintext}
    """
    results = {}
    for shift in range(26):
        results[shift] = decrypt(ciphertext, shift)
    return results
