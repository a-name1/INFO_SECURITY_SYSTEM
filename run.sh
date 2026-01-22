#!/bin/bash
# 信息安全技术系统 - 启动脚本

echo "================================================"
echo "  信息安全技术系统 - 启动脚本"
echo "================================================"
echo ""

# 检查Python版本
python_version=$(python --version 2>&1)
echo "检测到: $python_version"
echo ""

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
    echo "虚拟环境创建完成"
else
    echo "虚拟环境已存在"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
echo ""

# 安装依赖
echo "检查并安装依赖..."
pip install -q -r requirements.txt
echo "依赖安装完成"
echo ""

# 初始化数据库
if [ ! -f "database/users.db" ]; then
    echo "初始化数据库..."
    python database/init_db.py
    echo ""
fi

# 启动应用
echo "启动服务器..."
echo "访问 http://127.0.0.1:5000"
echo "按 Ctrl+C 停止服务器"
echo ""

python app.py
