"""
信息安全技术系统 - 主应用程序
Flask Web应用入口
"""
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from functools import wraps
import os
from config import *
from auth.auth_routes import auth_bp
from database.init_db import init_database


# 初始化Flask应用
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = SECRET_KEY

# 注册蓝图
app.register_blueprint(auth_bp)

# 初始化数据库
if not os.path.exists('database/users.db'):
    init_database()


def login_required(f):
    """登录检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ===================== 前端页面路由 =====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')


@app.route('/register')
def register_page():
    """注册页面"""
    return render_template('register.html')


@app.route('/classic')
@login_required
def classic_page():
    """经典密码算法页面"""
    return render_template('classic.html')


@app.route('/modern')
@login_required
def modern_page():
    """现代密码算法页面"""
    return render_template('modern.html')


@app.route('/image-share')
@login_required
def image_share_page():
    """图像分存页面"""
    return render_template('image_share.html')


@app.route('/help')
def help_page():
    """帮助和指南页面（无需登录）"""
    return render_template('help.html')


# ===================== 文件下载路由 =====================

@app.route('/outputs/<filename>')
@login_required
def download_output_file(filename):
    """下载输出文件（恢复的图像等）"""
    try:
        # 验证文件名格式，防止目录遍历攻击
        if '..' in filename or '/' in filename or not filename:
            return jsonify({'success': False, 'message': '无效的文件名'}), 400
        
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'success': False, 'message': '文件不存在'}), 404
        
        # 根据文件扩展名设置 MIME 类型
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.txt': 'text/plain',
            '.pdf': 'application/pdf'
        }
        file_ext = os.path.splitext(filename)[1].lower()
        mimetype = mime_types.get(file_ext, 'application/octet-stream')
        
        return send_from_directory(OUTPUT_FOLDER, filename, mimetype=mimetype)
    except Exception as e:
        return jsonify({'success': False, 'message': f'下载失败: {str(e)}'}), 500


# ===================== 经典密码算法API =====================

@app.route('/api/classic/caesar', methods=['POST'])
@login_required
def caesar_api():
    """凯撒密码加密/解密"""
    try:
        from crypto_classic.caesar import encrypt, decrypt
        
        data = request.get_json()
        text = data.get('text', '')
        shift = int(data.get('shift', 3))
        operation = data.get('operation', 'encrypt')  # 'encrypt' or 'decrypt'
        
        if not text:
            return jsonify({'success': False, 'message': '文本不能为空'}), 400
        
        if operation == 'encrypt':
            result = encrypt(text, shift)
        else:
            result = decrypt(text, shift)
        
        return jsonify({
            'success': True,
            'result': result,
            'shift': shift
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/classic/substitution', methods=['POST'])
@login_required
def substitution_api():
    """单表置换密码加密/解密"""
    try:
        from crypto_classic.substitution import encrypt, decrypt, generate_key
        
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key')
        operation = data.get('operation', 'encrypt')
        
        if not text:
            return jsonify({'success': False, 'message': '文本不能为空'}), 400
        
        # 如果没有提供密钥，生成新的
        if not key:
            key = generate_key()
        
        if operation == 'encrypt':
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)
        
        return jsonify({
            'success': True,
            'result': result,
            'key': key
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/classic/playfair', methods=['POST'])
@login_required
def playfair_api():
    """Playfair密码加密/解密"""
    try:
        from crypto_classic.playfair import encrypt, decrypt
        
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not text or not key:
            return jsonify({'success': False, 'message': '文本和密钥都不能为空'}), 400
        
        if operation == 'encrypt':
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


# ===================== 现代密码算法API =====================

@app.route('/api/modern/md5', methods=['POST'])
@login_required
def md5_api():
    """MD5哈希"""
    try:
        from crypto_modern.md5_hash import hash_text
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'message': '文本不能为空'}), 400
        
        hash_value = hash_text(text)
        
        return jsonify({
            'success': True,
            'hash': hash_value,
            'algorithm': 'MD5'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/modern/des', methods=['POST'])
@login_required
def des_api():
    """DES加密/解密"""
    try:
        from crypto_modern.des_cipher import encrypt, decrypt
        
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not text or not key:
            return jsonify({'success': False, 'message': '文本和密钥都不能为空'}), 400
        
        if operation == 'encrypt':
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)
        
        return jsonify({
            'success': True,
            'result': result,
            'algorithm': 'DES'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/modern/aes', methods=['POST'])
@login_required
def aes_api():
    """AES加密/解密"""
    try:
        from crypto_modern.aes_cipher import encrypt, decrypt
        
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        key_size = int(data.get('key_size', 32))
        
        if not text or not key:
            return jsonify({'success': False, 'message': '文本和密钥都不能为空'}), 400
        
        if operation == 'encrypt':
            result = encrypt(text, key, key_size)
        else:
            result = decrypt(text, key, key_size)
        
        return jsonify({
            'success': True,
            'result': result,
            'algorithm': 'AES',
            'key_size': key_size
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/modern/rsa/generate', methods=['POST'])
@login_required
def rsa_generate_api():
    """生成RSA密钥对"""
    try:
        from crypto_modern.rsa_cipher import RSAKeyPair
        
        data = request.get_json()
        key_size = int(data.get('key_size', 2048))
        
        keypair = RSAKeyPair(key_size)
        
        return jsonify({
            'success': True,
            'public_key': keypair.get_public_key_pem(),
            'private_key': keypair.get_private_key_pem(),
            'key_size': key_size
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/modern/rsa/encrypt', methods=['POST'])
@login_required
def rsa_encrypt_api():
    """RSA加密"""
    try:
        from crypto_modern.rsa_cipher import encrypt
        
        data = request.get_json()
        text = data.get('text', '')
        public_key = data.get('public_key', '')
        
        if not text or not public_key:
            return jsonify({'success': False, 'message': '文本和公钥都不能为空'}), 400
        
        result = encrypt(text, public_key)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@app.route('/api/modern/rsa/decrypt', methods=['POST'])
@login_required
def rsa_decrypt_api():
    """RSA解密"""
    try:
        from crypto_modern.rsa_cipher import decrypt
        
        data = request.get_json()
        text = data.get('text', '')
        private_key = data.get('private_key', '')
        
        if not text or not private_key:
            return jsonify({'success': False, 'message': '密文和私钥都不能为空'}), 400
        
        result = decrypt(text, private_key)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


# ===================== 图像分存API =====================

@app.route('/api/image/split', methods=['POST'])
@login_required
def image_split_api():
    """分割图像为多个分片（支持PNG、JPG、BMP等多种格式）"""
    try:
        from image_share.shamir_share import ShamirShare
        import time
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': '未上传图像'}), 400
        
        file = request.files['image']
        threshold = int(request.form.get('threshold', SHAMIR_THRESHOLD))
        shares = int(request.form.get('shares', SHAMIR_SHARES))
        
        if not file or file.filename == '':
            return jsonify({'success': False, 'message': '文件名为空'}), 400
        
        if threshold > shares or threshold < 2:
            return jsonify({'success': False, 'message': '无效的阈值参数（k必须≤n且≥2）'}), 400
        
        # 保存上传的图像
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)
        
        # 创建Shamir分片对象并分割图像
        shamir = ShamirShare(threshold=threshold, shares=shares)
        shares_dir = os.path.join(OUTPUT_FOLDER, f"shares_{timestamp}")
        os.makedirs(shares_dir, exist_ok=True)
        
        # split_image会自动保存metadata.json
        metadata = shamir.split_image(image_path, shares_dir)
        
        # 生成分片文件列表
        share_files = sorted([
            f for f in os.listdir(shares_dir) 
            if f.startswith('share_') and f.endswith('.bin')
        ], key=lambda x: int(x.split('_')[1].split('.')[0]))
        
        return jsonify({
            'success': True,
            'message': f'✅ 成功生成{shares}个分片，其中任意{threshold}个可恢复原图！系统已自动保存metadata.json',
            'timestamp': timestamp,
            'threshold': threshold,
            'total_shares': shares,
            'shares': share_files,
            'image_mode': metadata.get('mode', 'RGB'),
            'image_size': metadata.get('size', [0, 0]),
            'metadata_included': True,
            'download_hint': f'✨ 新功能：无需手动输入参数，恢复时自动从metadata.json读取所有信息'
        }), 200
    
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'message': f'分割失败: {str(e)}'}), 500


@app.route('/api/image/recover', methods=['POST'])
@login_required
def image_recover_api():
    """从分片恢复图像（自动检测格式和尺寸）"""
    try:
        from image_share.recover import recover_image_from_shares
        import time
        import tempfile
        import shutil
        import json
        
        # 获取上传的分片文件
        share_files_uploaded = request.files.getlist('share_files')
        
        if not share_files_uploaded or len(share_files_uploaded) == 0:
            return jsonify({'success': False, 'message': '未上传任何分片文件'}), 400
        
        # 临时目录用于存储分片
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 保存上传的分片文件
            share_files = []
            metadata_file = None
            
            for f in share_files_uploaded:
                if f and f.filename:
                    temp_path = os.path.join(temp_dir, f.filename)
                    f.save(temp_path)
                    
                    if f.filename == 'metadata.json':
                        metadata_file = temp_path
                    else:
                        share_files.append(temp_path)
            
            if len(share_files) == 0:
                return jsonify({'success': False, 'message': '没有有效的分片文件（.bin格式）'}), 400
            
            # 检查metadata.json
            if metadata_file is None:
                return jsonify({
                    'success': False, 
                    'message': '❌ 缺失metadata.json文件！恢复需要此文件以获取图像参数。请确保上传了metadata.json文件。'
                }), 400
            
            # 恢复图像（recover_image_from_shares会自动从metadata.json读取参数）
            timestamp = int(time.time())
            output_filename = f"recovered_{timestamp}.png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            # 调用恢复函数 - 自动加载metadata.json
            recovered_file = recover_image_from_shares(temp_dir, output_path)
            
            # 验证恢复成功
            if not os.path.exists(recovered_file):
                return jsonify({
                    'success': False, 
                    'message': '恢复过程中出错：无法生成输出文件'
                }), 500
            
            # 读取元数据以返回给前端
            metadata_info = {}
            if metadata_file and os.path.exists(metadata_file):
                with open(metadata_file, 'r') as mf:
                    metadata_info = json.load(mf)
            
            return jsonify({
                'success': True,
                'message': '✅ 图像恢复成功！',
                'output_file': output_filename,
                'download_url': f'/outputs/{output_filename}',
                'share_count': len(share_files),
                'metadata': metadata_info,
                'note': '系统已从上传的分片自动恢复出原始图像'
            }), 200
        
        finally:
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    except FileNotFoundError as e:
        return jsonify({'success': False, 'message': f'❌ 文件错误：{str(e)}'}), 400
    except ValueError as e:
        return jsonify({'success': False, 'message': f'❌ 参数错误：{str(e)}'}), 400
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'message': f'❌ 恢复失败: {str(e)}'}), 500


# ===================== 错误处理 =====================

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'success': False, 'message': '页面不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'success': False, 'message': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
