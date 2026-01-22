import numpy as np
from PIL import Image
import os
import json
import struct # 引入 struct 处理双字节存储

class ShamirShare:
    def __init__(self, threshold: int = 3, shares: int = 5):
        if threshold > shares:
            raise ValueError("阈值(k)不能大于总分片数(n)")
        self.threshold = threshold
        self.shares = shares
        self.prime = 257  # 使用257作为素数，确保覆盖0-255字节范围

    def _reconstruct_secret(self, shares_data: list) -> bytes:
        """
        修正版：支持从 0-265 范围的分片数据恢复 0-255 的原始字节
        """
        # 确保只使用阈值数量的分片
        shares_data = shares_data[:self.threshold]
        # 注意：此时 shares_data[i][1] 是存储了 0-256 整数的列表或数组
        data_len = len(shares_data[0][1])
        secret = bytearray()

        for byte_index in range(data_len):
            secret_value = 0
            for i in range(self.threshold):
                xi, yi = shares_data[i][0], shares_data[i][1][byte_index]
                
                # 计算拉格朗日基函数 L_i(0)
                num, den = 1, 1
                for j in range(self.threshold):
                    if i != j:
                        xj = shares_data[j][0]
                        # L_i(0) = ∏ (-xj) / (xi - xj)
                        num = (num * -xj) % self.prime
                        den = (den * (xi - xj)) % self.prime
                
                # 模逆运算获取分母在 GF(257) 下的倒数
                den_inv = pow(den, self.prime - 2, self.prime)
                basis = (num * den_inv) % self.prime
                
                # 累加：secret = ∑ yi * L_i(0)
                secret_value = (secret_value + yi * basis) % self.prime
            
            # 此时 secret_value 必然在 0-255 之间（因为原始输入就在此范围）
            secret.append(secret_value)
        
        return bytes(secret)

    def split_image(self, image_path: str, output_dir: str):
        """
        修正版：使用双字节存储分片数据，解决 256 溢出导致的字节不匹配问题
        """
        img = Image.open(image_path)
        metadata = {
            "mode": img.mode,
            "size": img.size,
            "threshold": self.threshold,
            "shares": self.shares
        }
        
        img_bytes = img.tobytes()
        os.makedirs(output_dir, exist_ok=True)
        
        # 存储 0-256 的整数列表
        shares_values = [[] for _ in range(self.shares)]

        for byte_val in img_bytes:
            # 秘密 a0 = byte_val (0-255)
            coeffs = [byte_val] + [int(os.urandom(1)[0]) for _ in range(self.threshold - 1)]
            
            for x in range(1, self.shares + 1):
                y = 0
                for idx, a in enumerate(coeffs):
                    y = (y + a * pow(x, idx, self.prime)) % self.prime
                # y 的取值范围是 0-256
                shares_values[x-1].append(y)

        # 保存分片：使用 'H' (unsigned short, 2 bytes) 确保 256 不丢失
        for i, values in enumerate(shares_values):
            share_path = os.path.join(output_dir, f"share_{i+1}.bin")
            with open(share_path, 'wb') as f:
                # 使用 struct 将整数列表打包为二进制
                # 'H' 代表 16 位无符号整数，'<' 代表小端序
                f.write(struct.pack(f"<{len(values)}H", *values))

        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f)
            
        return metadata