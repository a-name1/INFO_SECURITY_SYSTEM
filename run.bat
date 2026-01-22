@echo off
REM 信息安全技术系统 - Windows启动脚本

echo ================================================
echo   信息安全技术系统 - 启动脚本
echo ================================================
echo.

REM 检查Python版本
python --version
echo.

REM 创建虚拟环境（如果不存在）
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成
) else (
    echo 虚拟环境已存在
)
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat
echo.

REM 安装依赖
echo 检查并安装依赖...
pip install -q -r requirements.txt
echo 依赖安装完成
echo.

REM 初始化数据库
if not exist "database\users.db" (
    echo 初始化数据库...
    python database\init_db.py
    echo.
)

REM 启动应用
echo 启动服务器...
echo 访问 http://127.0.0.1:5000
echo 按 Ctrl+C 停止服务器
echo.

python app.py
pause
