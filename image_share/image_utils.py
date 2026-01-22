from PIL import Image
import os

def read_image(image_path: str) -> Image.Image:
    """读取图像并保留所有通道（如PNG的透明度通道）"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件不存在: {image_path}")
    return Image.open(image_path)

def save_image(image: Image.Image, output_path: str):
    """保存恢复后的图像，自动处理输出路径"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)