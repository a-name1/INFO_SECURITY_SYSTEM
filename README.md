# 信息安全技术课程设计系统

## 一、 项目概述
[cite_start]本项目为《信息安全技术》课程的期末考查项目。系统采用 **B/S（Browser/Server）架构**，集成了一个具有身份认证功能的 Web 平台，实现了经典密码算法、现代密码算法以及图像信息分存技术。

## 二、 快速开始 (Quick Start)

### 1. 环境准备
确保您的系统已安装 **Python 3.8+**。建议创建虚拟环境以运行：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

```

### 2. 安装必要依赖

本系统依赖 Flask 框架、PyCryptodome 加密库及图像处理库 ：

```bash
pip install flask pycryptodome Pillow opencv-python

```

### 3. 初始化与运行

1. **数据库初始化：** 运行 `python database/init_db.py` 以创建用户认证数据库。
2. **启动服务器：** 运行 `python app.py`。
3. **访问系统：** 在浏览器中打开 `http://127.0.0.1:5000`。

---

## 三、 系统架构设计 

系统采用 **B/S 架构**，主要包括以下层次：

* **表现层：** 基于 HTML/CSS/JS 的 Web 前端界面，负责用户交互。
* **业务逻辑层：** Flask 后端控制层，负责调用各加解密模块。
* **数据存储层：** SQLite 数据库，用于保存用户信息及认证凭证。

---

## 四、 功能模块细则 

### 4.1 身份认证模块 (Auth)

* 提供用户注册与认证登录功能 。

* 使用 **MD5** 算法对用户密码进行哈希处理后存储，确保数据库安全性 。

### 4.2 经典密码算法模块 (Crypto Classic)

实现本学期课堂教授的经典密码：

* **凯撒密码 (Caesar)**
* **单表置换密码**
* **Playfair 密码**

### 4.3 现代密码算法模块 (Crypto Modern)

实现业界主流的现代密码技术：

* **对称加密：** DES、AES
* **非对称加密：** RSA
* **摘要算法：** MD5

### 4.4 图像信息分存模块 (Image Share)

* 实现图像信息的加密分存算法 。

* 支持将原始图像分解为多个子图像，并可通过满足条件的子图像组合恢复原图 。

## 五、 项目目录结构

```text
info_security_system/
├── app.py              # 系统主入口
├── config.py           # 集中管理“全局配置参数”
├── auth/               # 身份认证模块（登录/注册）
├── crypto_classic/     # 经典密码算法实现
├── crypto_modern/      # 现代密码算法实现
├── image_share/        # 图像信息分存模块
├── templates/          # 前端 HTML 页面
├── static/             # 静态资源（CSS/JS/Images）
├── database/           # 数据库及初始化脚本
├── uploads/            # 用于存放用户上传的原始图像文件
├── outputs/            # 用于存放系统生成的输出结果
└── README.md           # 项目说明文档
```

## 六、 总结

本系统严格按照课程大纲要求开发，主要训练自主学习能力，并对学术规范进行初步训练 。

