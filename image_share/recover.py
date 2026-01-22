from image_share.shamir_share import ShamirShare
import os
import json
from PIL import Image
import struct

def recover_image_from_shares(share_dir: str, output_path: str) -> str:
    """从包含分片和元数据的目录自动恢复图像 (支持双字节解包)"""
    
    # 1. 加载元数据
    metadata_path = os.path.join(share_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"在目录 {share_dir} 中缺失元数据文件 metadata.json")

    with open(metadata_path, 'r') as f:
        meta = json.load(f)

    # 2. 自动检索分片文件 (.bin)
    share_files = [
        os.path.join(share_dir, f) 
        for f in os.listdir(share_dir) 
        if f.startswith("share_") and f.endswith(".bin")
    ]

    if len(share_files) < meta['threshold']:
        raise ValueError(f"分片不足。需要 {meta['threshold']} 个，实际找到 {len(share_files)} 个")

    # 3. 读取并解包分片数据
    shares_data = []
    # 按照阈值要求的数量读取（取前 k 个）
    for sf in share_files[:meta['threshold']]:
        # 从文件名解析 x 坐标 (例如 share_1.bin -> x=1)
        try:
            x = int(os.path.basename(sf).split('_')[1].split('.')[0])
        except (IndexError, ValueError):
            continue
            
        with open(sf, 'rb') as f:
            binary_data = f.read()
            # 关键修复：计算 uint16 的个数 (每个像素占2字节)
            count = len(binary_data) // 2
            # '<' 小端序, 'H' 无符号短整型 (uint16)
            # 解包后得到 0-256 范围的整数列表
            y_values = struct.unpack(f"<{count}H", binary_data)
            shares_data.append((x, y_values))

    # 4. 初始化 Shamir 核心类并执行拉格朗日插值
    shamir = ShamirShare(threshold=meta['threshold'], shares=len(share_files))
    
    try:
        # 调用之前修正过的 _reconstruct_secret
        recovered_bytes = shamir._reconstruct_secret(shares_data)
        
        # 5. 根据元数据重组图像
        # recovered_bytes 长度应等于 width * height * channels
        img = Image.frombytes(meta['mode'], tuple(meta['size']), recovered_bytes)
        img.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"恢复图像时发生错误: {str(e)}")

def validate_shares(share_dir: str) -> bool:
    """简单的分片完整性验证"""
    metadata_path = os.path.join(share_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        return False
    return len([f for f in os.listdir(share_dir) if f.endswith('.bin')]) > 0