"""
Playfair密码
使用5x5矩阵的经典密码算法
"""

def _prepare_text(text: str) -> str:
    """
    预处理文本：移除空格和标点，转换为大写，用J替换I
    """
    text = text.upper().replace('J', 'I')
    text = ''.join(char for char in text if char.isalpha())
    return text


def _find_position(matrix: list, char: str) -> tuple:
    """在5x5矩阵中查找字符位置"""
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return (i, j)
    return None


def _create_matrix(key: str) -> list:
    """
    创建Playfair矩阵
    
    Args:
        key: 密钥
    
    Returns:
        5x5字符矩阵
    """
    key = _prepare_text(key)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 没有J
    
    # 去除密钥中的重复字母
    seen = set()
    matrix_chars = []
    for char in key:
        if char not in seen:
            matrix_chars.append(char)
            seen.add(char)
    
    # 添加字母表中的其他字母
    for char in alphabet:
        if char not in seen:
            matrix_chars.append(char)
    
    # 构建5x5矩阵
    matrix = []
    for i in range(5):
        matrix.append(matrix_chars[i*5:(i+1)*5])
    
    return matrix


def _encrypt_pair(matrix: list, char1: str, char2: str) -> str:
    """加密一对字母"""
    row1, col1 = _find_position(matrix, char1)
    row2, col2 = _find_position(matrix, char2)
    
    if row1 == row2:
        # 同行：向右循环移动
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        # 同列：向下循环移动
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        # 矩形：交换列
        return matrix[row1][col2] + matrix[row2][col1]


def _decrypt_pair(matrix: list, char1: str, char2: str) -> str:
    """解密一对字母"""
    row1, col1 = _find_position(matrix, char1)
    row2, col2 = _find_position(matrix, char2)
    
    if row1 == row2:
        # 同行：向左循环移动
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        # 同列：向上循环移动
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        # 矩形：交换列
        return matrix[row1][col2] + matrix[row2][col1]


def encrypt(plaintext: str, key: str) -> str:
    """
    Playfair加密
    
    Args:
        plaintext: 明文
        key: 密钥
    
    Returns:
        密文
    """
    matrix = _create_matrix(key)
    plaintext = _prepare_text(plaintext)
    
    # 如果长度为奇数，添加X
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    
    ciphertext = []
    for i in range(0, len(plaintext), 2):
        char1 = plaintext[i]
        char2 = plaintext[i + 1]
        
        # 如果两个字母相同，插入X
        if char1 == char2:
            char2 = 'X'
            ciphertext.append(_encrypt_pair(matrix, char1, char2))
            ciphertext.append(plaintext[i + 1])
        else:
            ciphertext.append(_encrypt_pair(matrix, char1, char2))
    
    return ''.join(ciphertext)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Playfair解密
    
    Args:
        ciphertext: 密文
        key: 密钥
    
    Returns:
        明文
    """
    matrix = _create_matrix(key)
    ciphertext = _prepare_text(ciphertext)
    
    plaintext = []
    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]
        plaintext.append(_decrypt_pair(matrix, char1, char2))
    
    return ''.join(plaintext)
