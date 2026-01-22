#!/usr/bin/env python3
"""
高级图像分割测试套件
支持多种配置和测试场景
"""

import os
import sys
import json
import time
from pathlib import Path
from PIL import Image
from typing import List, Tuple, Dict

sys.path.insert(0, str(Path(__file__).parent))

from image_share.shamir_share import ShamirShare
from image_share.recover import recover_image_from_shares


class ImageSplitTestSuite:
    """图像分割测试套件"""
    
    def __init__(self, base_dir: str = './test_suite_output'):
        """
        初始化测试套件
        
        Args:
            base_dir: 测试输出基础目录
        """
        self.base_dir = base_dir
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'details': []
        }
        os.makedirs(base_dir, exist_ok=True)
    
    def create_test_image(
        self,
        filename: str,
        width: int = 256,
        height: int = 256,
        mode: str = 'RGB'
    ) -> str:
        """
        创建测试图像
        
        Args:
            filename: 图像文件名
            width: 图像宽度
            height: 图像高度
            mode: 图像模式 (RGB, RGBA, L 等)
        
        Returns:
            str: 图像完整路径
        """
        image_path = os.path.join(self.base_dir, filename)
        
        if mode == 'RGB':
            img = Image.new('RGB', (width, height))
            pixels = img.load()
            for y in range(height):
                for x in range(width):
                    r = int(255 * x / width)
                    g = int(255 * y / height)
                    b = 128
                    pixels[x, y] = (r, g, b)
        
        elif mode == 'RGBA':
            img = Image.new('RGBA', (width, height))
            pixels = img.load()
            for y in range(height):
                for x in range(width):
                    r = int(255 * x / width)
                    g = int(255 * y / height)
                    b = 128
                    a = int(255 * (1 - x / width))
                    pixels[x, y] = (r, g, b, a)
        
        elif mode == 'L':
            img = Image.new('L', (width, height))
            pixels = img.load()
            for y in range(height):
                for x in range(width):
                    gray = int(255 * (x + y) / (width + height) / 2)
                    pixels[x, y] = gray
        
        else:
            raise ValueError(f"不支持的图像模式: {mode}")
        
        img.save(image_path)
        return image_path
    
    def run_basic_test(self, test_name: str, config: Dict) -> bool:
        """
        运行基础测试
        
        Args:
            test_name: 测试名称
            config: 测试配置字典，包含:
                - image_size: (width, height)
                - image_mode: RGB|RGBA|L
                - threshold: k 值
                - total_shares: n 值
        
        Returns:
            bool: 测试是否通过
        """
        self.results['total_tests'] += 1
        start_time = time.time()
        
        try:
            # 创建测试目录
            test_dir = os.path.join(self.base_dir, test_name)
            os.makedirs(test_dir, exist_ok=True)
            
            # 提取配置
            width, height = config.get('image_size', (256, 256))
            image_mode = config.get('image_mode', 'RGB')
            threshold = config.get('threshold', 3)
            total_shares = config.get('total_shares', 5)
            
            print(f"\n🧪 测试: {test_name}")
            print(f"   配置: {width}×{height} {image_mode}, k={threshold}, n={total_shares}")
            
            # 1. 创建测试图像
            image_path = self.create_test_image(
                os.path.join(test_name, 'original.png'),
                width=width,
                height=height,
                mode=image_mode
            )
            
            # 2. 分割图像
            shamir = ShamirShare(threshold=threshold, shares=total_shares)
            metadata = shamir.split_image(image_path, test_dir)
            
            # 3. 恢复图像
            recovered_path = os.path.join(test_dir, 'recovered.png')
            recover_image_from_shares(test_dir, recovered_path)
            
            # 4. 比较图像
            original = Image.open(image_path)
            recovered = Image.open(recovered_path)
            
            if original.size != recovered.size or original.mode != recovered.mode:
                raise ValueError("图像尺寸或模式不匹配")
            
            # 计算精度
            orig_pixels = list(original.getdata())
            rec_pixels = list(recovered.getdata())
            
            total = len(orig_pixels)
            matching = sum(1 for o, r in zip(orig_pixels, rec_pixels) if o == r)
            accuracy = matching / total * 100
            
            elapsed_time = time.time() - start_time
            
            result = {
                'test': test_name,
                'status': '✅ 通过',
                'accuracy': f"{accuracy:.2f}%",
                'time': f"{elapsed_time:.2f}s",
                'config': config
            }
            
            self.results['passed'] += 1
            self.results['details'].append(result)
            
            print(f"   ✅ 通过 (精度: {accuracy:.2f}%, 耗时: {elapsed_time:.2f}s)")
            return True
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            
            result = {
                'test': test_name,
                'status': f'❌ 失败: {str(e)}',
                'time': f"{elapsed_time:.2f}s",
                'config': config
            }
            
            self.results['failed'] += 1
            self.results['details'].append(result)
            
            print(f"   ❌ 失败: {e}")
            return False
    
    def run_stress_test(
        self,
        test_name: str,
        image_sizes: List[Tuple[int, int]],
        threshold: int = 3,
        total_shares: int = 5
    ) -> Dict:
        """
        运行压力测试
        
        Args:
            test_name: 测试名称
            image_sizes: 图像尺寸列表 [(width, height), ...]
            threshold: k 值
            total_shares: n 值
        
        Returns:
            dict: 测试结果
        """
        print(f"\n📊 压力测试: {test_name}")
        print(f"   测试 {len(image_sizes)} 种图像尺寸")
        
        results = {
            'sizes': [],
            'total_time': 0
        }
        
        for width, height in image_sizes:
            config = {
                'image_size': (width, height),
                'image_mode': 'RGB',
                'threshold': threshold,
                'total_shares': total_shares
            }
            
            sub_test_name = f"{test_name}_{width}x{height}"
            success = self.run_basic_test(sub_test_name, config)
            
            if success:
                # 获取时间信息
                for detail in self.results['details']:
                    if detail['test'] == sub_test_name:
                        time_str = detail['time'].replace('s', '')
                        results['sizes'].append({
                            'size': (width, height),
                            'time': float(time_str)
                        })
                        results['total_time'] += float(time_str)
                        break
        
        print(f"   总耗时: {results['total_time']:.2f}s")
        return results
    
    def run_config_test(
        self,
        test_name: str,
        configs: List[Dict]
    ) -> Dict:
        """
        运行配置测试（测试不同的 k/n 组合）
        
        Args:
            test_name: 测试名称
            configs: 配置列表
        
        Returns:
            dict: 测试结果
        """
        print(f"\n⚙️  配置测试: {test_name}")
        print(f"   测试 {len(configs)} 种配置")
        
        results = {
            'configurations': []
        }
        
        for i, config in enumerate(configs):
            sub_test_name = f"{test_name}_config_{i+1}"
            success = self.run_basic_test(sub_test_name, config)
            
            if success:
                for detail in self.results['details']:
                    if detail['test'] == sub_test_name:
                        results['configurations'].append({
                            'config': f"k={config['threshold']}/n={config['total_shares']}",
                            'accuracy': detail['accuracy'],
                            'time': detail['time']
                        })
                        break
        
        return results
    
    def print_summary(self):
        """打印测试总结"""
        print("\n╔════════════════════════════════════════════════╗")
        print("║            测试套件总结                        ║")
        print("╚════════════════════════════════════════════════╝")
        
        total = self.results['total_tests']
        passed = self.results['passed']
        failed = self.results['failed']
        
        print(f"\n📊 统计:")
        print(f"   总测试数: {total}")
        print(f"   ✅ 通过: {passed}")
        print(f"   ❌ 失败: {failed}")
        
        if total > 0:
            pass_rate = (passed / total) * 100
            print(f"   通过率: {pass_rate:.1f}%")
        
        print(f"\n📋 详细结果:")
        for detail in self.results['details']:
            print(f"   {detail['test']}")
            print(f"      状态: {detail['status']}")
            if 'accuracy' in detail:
                print(f"      精度: {detail['accuracy']}")
            print(f"      耗时: {detail['time']}")
    
    def save_report(self, filename: str = 'test_report.json'):
        """
        保存测试报告
        
        Args:
            filename: 报告文件名
        """
        report_path = os.path.join(self.base_dir, filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 测试报告已保存: {report_path}")


def main():
    """主函数"""
    
    print("╔════════════════════════════════════════════════╗")
    print("║     图像分割高级测试套件                       ║")
    print("╚════════════════════════════════════════════════╝")
    
    # 创建测试套件
    suite = ImageSplitTestSuite('./test_suite_output')
    
    # 1. 基础测试 - 不同图像模式
    print("\n[1/4] 基础测试 - 图像模式")
    suite.run_basic_test('basic_rgb', {
        'image_size': (256, 256),
        'image_mode': 'RGB',
        'threshold': 3,
        'total_shares': 5
    })
    
    suite.run_basic_test('basic_rgba', {
        'image_size': (256, 256),
        'image_mode': 'RGBA',
        'threshold': 3,
        'total_shares': 5
    })
    
    suite.run_basic_test('basic_grayscale', {
        'image_size': (256, 256),
        'image_mode': 'L',
        'threshold': 3,
        'total_shares': 5
    })
    
    # 2. 配置测试 - 不同的 k/n 组合
    print("\n[2/4] 配置测试 - k/n 组合")
    configs = [
        {'image_size': (256, 256), 'image_mode': 'RGB', 'threshold': 2, 'total_shares': 3},
        {'image_size': (256, 256), 'image_mode': 'RGB', 'threshold': 3, 'total_shares': 5},
        {'image_size': (256, 256), 'image_mode': 'RGB', 'threshold': 4, 'total_shares': 7},
        {'image_size': (256, 256), 'image_mode': 'RGB', 'threshold': 5, 'total_shares': 10},
    ]
    suite.run_config_test('config_variants', configs)
    
    # 3. 压力测试 - 不同图像尺寸
    print("\n[3/4] 压力测试 - 图像尺寸")
    sizes = [(128, 128), (256, 256), (512, 512)]
    suite.run_stress_test('stress_sizes', sizes)
    
    # 4. 边界测试
    print("\n[4/4] 边界测试")
    suite.run_basic_test('edge_small', {
        'image_size': (32, 32),
        'image_mode': 'RGB',
        'threshold': 2,
        'total_shares': 3
    })
    
    suite.run_basic_test('edge_large', {
        'image_size': (1024, 1024),
        'image_mode': 'RGB',
        'threshold': 3,
        'total_shares': 5
    })
    
    # 打印总结和保存报告
    suite.print_summary()
    suite.save_report()
    
    # 返回状态码
    return 0 if suite.results['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
