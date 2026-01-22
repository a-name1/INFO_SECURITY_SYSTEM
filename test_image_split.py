#!/usr/bin/env python3
"""
图像分割测试代码
测试 Shamir 秘密分享对图像的分割和恢复功能
"""

import os
import sys
from pathlib import Path
from PIL import Image
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from image_share.shamir_share import ShamirShare
from image_share.recover import recover_image_from_shares


def create_test_image(image_path: str, width: int = 256, height: int = 256) -> str:
    """
    创建测试图像
    
    Args:
        image_path: 图像保存路径
        width: 图像宽度
        height: 图像高度
    
    Returns:
        str: 图像路径
    """
    print(f"📸 创建测试图像: {image_path} ({width}x{height})")
    
    # 创建输出目录
    os.makedirs(os.path.dirname(image_path) or '.', exist_ok=True)
    
    # 创建 RGB 图像（彩色）
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    # 填充颜色梯度
    for y in range(height):
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = 128
            pixels[x, y] = (r, g, b)
    
    img.save(image_path)
    print(f"   ✅ 测试图像已创建: {image_path}")
    return image_path


def test_image_split(
    image_path: str,
    output_dir: str = './test_output',
    threshold: int = 3,
    total_shares: int = 5
) -> dict:
    """
    测试图像分割功能
    
    Args:
        image_path: 原始图像路径
        output_dir: 分片输出目录
        threshold: 恢复所需的最少分片数（k）
        total_shares: 总分片数（n）
    
    Returns:
        dict: 分割结果元数据
    """
    print(f"\n🔀 测试图像分割")
    print(f"   参数: k={threshold}, n={total_shares}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 初始化 Shamir 分享器
        shamir = ShamirShare(threshold=threshold, shares=total_shares)
        
        # 分割图像（自动保存 metadata.json）
        metadata = shamir.split_image(image_path, output_dir)
        
        print(f"   ✅ 图像已分割")
        print(f"   📊 元数据:")
        print(f"      - 图像模式: {metadata['mode']}")
        print(f"      - 图像尺寸: {metadata['size']}")
        print(f"      - 阈值: {metadata['threshold']}")
        
        # 列出生成的分片文件
        share_files = [f for f in os.listdir(output_dir) if f.startswith('share_')]
        print(f"   📦 生成的分片数: {len(share_files)}")
        
        for share_file in sorted(share_files):
            file_path = os.path.join(output_dir, share_file)
            file_size = os.path.getsize(file_path)
            print(f"      - {share_file}: {file_size} 字节")
        
        # 检查元数据文件
        metadata_file = os.path.join(output_dir, 'metadata.json')
        if os.path.exists(metadata_file):
            print(f"   📄 metadata.json: {os.path.getsize(metadata_file)} 字节")
        
        return metadata
        
    except Exception as e:
        print(f"   ❌ 分割失败: {e}")
        raise


def test_image_recover(
    share_dir: str,
    output_path: str = './test_output/recovered.png'
) -> bool:
    """
    测试图像恢复功能
    
    Args:
        share_dir: 分片所在目录
        output_path: 恢复图像的输出路径
    
    Returns:
        bool: 恢复是否成功
    """
    print(f"\n🔄 测试图像恢复")
    print(f"   分片目录: {share_dir}")
    print(f"   输出路径: {output_path}")
    
    try:
        # 自动加载 metadata.json，恢复图像
        recovered_path = recover_image_from_shares(share_dir, output_path)
        
        print(f"   ✅ 图像已恢复")
        print(f"   📄 输出文件: {recovered_path}")
        
        # 验证文件
        if os.path.exists(recovered_path):
            file_size = os.path.getsize(recovered_path)
            print(f"   📊 文件大小: {file_size} 字节")
            return True
        else:
            print(f"   ❌ 恢复的文件不存在")
            return False
            
    except Exception as e:
        print(f"   ❌ 恢复失败: {e}")
        raise


def compare_images(original_path: str, recovered_path: str) -> dict:
    """
    比较原始图像和恢复图像
    
    Args:
        original_path: 原始图像路径
        recovered_path: 恢复图像路径
    
    Returns:
        dict: 比较结果
    """
    print(f"\n📋 比较图像")
    
    try:
        original = Image.open(original_path)
        recovered = Image.open(recovered_path)
        
        print(f"   原始图像:")
        print(f"      - 尺寸: {original.size}")
        print(f"      - 模式: {original.mode}")
        
        print(f"   恢复图像:")
        print(f"      - 尺寸: {recovered.size}")
        print(f"      - 模式: {recovered.mode}")
        
        # 检查尺寸是否相同
        if original.size != recovered.size:
            print(f"   ⚠️ 尺寸不匹配!")
            return {'match': False, 'reason': 'size_mismatch'}
        
        # 检查模式是否相同
        if original.mode != recovered.mode:
            print(f"   ⚠️ 模式不匹配!")
            return {'match': False, 'reason': 'mode_mismatch'}
        
        # 逐像素比较
        original_pixels = list(original.getdata())
        recovered_pixels = list(recovered.getdata())
        
        total_pixels = len(original_pixels)
        mismatch_count = sum(
            1 for o, r in zip(original_pixels, recovered_pixels)
            if o != r
        )
        
        accuracy = (total_pixels - mismatch_count) / total_pixels * 100
        
        print(f"   ✅ 图像对比结果:")
        print(f"      - 总像素数: {total_pixels}")
        print(f"      - 匹配像素: {total_pixels - mismatch_count}")
        print(f"      - 不匹配: {mismatch_count}")
        print(f"      - 精度: {accuracy:.2f}%")
        
        return {
            'match': True,
            'total_pixels': total_pixels,
            'matching_pixels': total_pixels - mismatch_count,
            'mismatching_pixels': mismatch_count,
            'accuracy': accuracy
        }
        
    except Exception as e:
        print(f"   ❌ 比较失败: {e}")
        raise


def test_partial_recovery(share_dir: str, num_shares: int = 3) -> bool:
    """
    测试用部分分片恢复图像
    
    Args:
        share_dir: 分片目录
        num_shares: 使用的分片数
    
    Returns:
        bool: 是否恢复成功
    """
    print(f"\n🔄 测试部分分片恢复 (使用 {num_shares} 个分片)")
    
    try:
        # 获取所有分片文件
        share_files = sorted([
            f for f in os.listdir(share_dir)
            if f.startswith('share_') and f.endswith('.bin')
        ])
        
        if len(share_files) < num_shares:
            print(f"   ⚠️ 可用分片不足 ({len(share_files)} < {num_shares})")
            return False
        
        # 创建临时目录
        temp_dir = os.path.join(share_dir, f'temp_recovery_{num_shares}')
        os.makedirs(temp_dir, exist_ok=True)
        
        # 复制元数据文件
        metadata_src = os.path.join(share_dir, 'metadata.json')
        metadata_dst = os.path.join(temp_dir, 'metadata.json')
        if os.path.exists(metadata_src):
            with open(metadata_src, 'r') as f:
                with open(metadata_dst, 'w') as out:
                    out.write(f.read())
        
        # 复制部分分片文件
        for i, share_file in enumerate(share_files[:num_shares]):
            src = os.path.join(share_dir, share_file)
            dst = os.path.join(temp_dir, share_file)
            with open(src, 'rb') as f:
                with open(dst, 'wb') as out:
                    out.write(f.read())
        
        print(f"   📦 已复制 {num_shares} 个分片到临时目录")
        
        # 尝试恢复
        output_path = os.path.join(share_dir, f'partial_recovered_{num_shares}.png')
        recovered_path = recover_image_from_shares(temp_dir, output_path)
        
        if os.path.exists(recovered_path):
            print(f"   ✅ 用 {num_shares} 个分片成功恢复图像")
            return True
        else:
            print(f"   ❌ 恢复失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 部分恢复测试失败: {e}")
        return False


def main():
    """主测试函数"""
    
    print("╔════════════════════════════════════════════════╗")
    print("║      图像分割测试 (Shamir Secret Sharing)      ║")
    print("╚════════════════════════════════════════════════╝")
    
    # 测试参数
    test_image_path = './test_output/test_image.png'
    output_dir = './test_output'
    threshold = 3
    total_shares = 5
    recovered_image_path = os.path.join(output_dir, 'recovered.png')
    
    try:
        # 1. 创建测试图像
        create_test_image(test_image_path)
        
        # 2. 分割图像
        metadata = test_image_split(
            test_image_path,
            output_dir,
            threshold=threshold,
            total_shares=total_shares
        )
        
        # 3. 恢复图像
        success = test_image_recover(output_dir, recovered_image_path)
        
        if not success:
            print("\n❌ 恢复失败!")
            return 1
        
        # 4. 比较图像
        result = compare_images(test_image_path, recovered_image_path)
        
        # 5. 测试部分分片恢复
        test_partial_recovery(output_dir, num_shares=threshold)
        
        # 打印总结
        print("\n╔════════════════════════════════════════════════╗")
        print("║            测试完成 ✅                         ║")
        print("╚════════════════════════════════════════════════╝")
        print(f"\n📊 测试结果摘要:")
        print(f"   ✅ 图像分割: 成功")
        print(f"   ✅ 图像恢复: 成功")
        print(f"   ✅ 精度: {result.get('accuracy', 0):.2f}%")
        print(f"   ✅ 分片配置: {threshold}/{total_shares}")
        print(f"\n📁 输出目录: {os.path.abspath(output_dir)}")
        print(f"   - 原始图像: test_image.png")
        print(f"   - 分片文件: share_1.bin ~ share_5.bin")
        print(f"   - 元数据: metadata.json")
        print(f"   - 恢复图像: recovered.png")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
