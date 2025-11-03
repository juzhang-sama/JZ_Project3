# 第一阶段设置说明

## 📋 概述

本文档提供了第一阶段基础设施搭建的详细步骤。

**预计时间**：3-4天
**工作量**：40小时  

---

## 🚀 第1步：后端项目设置（2小时）

### 1.1 创建虚拟环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 1.2 安装依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装所有依赖
pip install -r requirements.txt
```

### 1.3 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件
# 重要：修改以下内容
# - DATABASE_URL: 数据库连接字符串
# - SECRET_KEY: JWT密钥（生成随机字符串）
# - COMFYUI_URL: ComfyUI服务地址
```

### 1.4 验证安装

```bash
# 测试导入
python -c "from app.config import settings; print('Config loaded successfully')"

# 测试数据库连接
python -c "from app.database import engine; print('Database connection OK')"
```

---

## 🗄️ 第2步：数据库设置（1小时）

### 2.1 创建PostgreSQL数据库

```bash
# 连接PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE image_gen_dev;

# 创建用户
CREATE USER image_gen WITH PASSWORD 'your_secure_password';

# 配置权限
ALTER ROLE image_gen SET client_encoding TO 'utf8';
ALTER ROLE image_gen SET default_transaction_isolation TO 'read committed';
ALTER ROLE image_gen SET default_transaction_deferrable TO on;

# 授予权限
GRANT ALL PRIVILEGES ON DATABASE image_gen_dev TO image_gen;

# 退出
\q
```

### 2.2 执行初始化脚本

```bash
# 执行SQL脚本
psql -U image_gen -d image_gen_dev -f backend/init_db.sql

# 验证表创建
psql -U image_gen -d image_gen_dev -c "\dt"
```

### 2.3 验证数据

```bash
# 查看模型数据
psql -U image_gen -d image_gen_dev -c "SELECT * FROM models;"

# 查看表结构
psql -U image_gen -d image_gen_dev -c "\d users"
```

---

## 🚀 第3步：启动后端服务（30分钟）

### 3.1 启动FastAPI

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 启动服务
uvicorn app.main:app --reload
```

### 3.2 验证API

```bash
# 在另一个终端测试
curl http://localhost:8000/health

# 访问API文档
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

---

## 📱 第4步：前端项目设置（1.5小时）

### 4.1 创建Flutter项目

```bash
# 创建项目
flutter create image_gen_app

# 进入项目目录
cd image_gen_app
```

### 4.2 配置依赖

```bash
# 复制pubspec.yaml
# 从 frontend/pubspec.yaml 复制到 image_gen_app/pubspec.yaml

# 获取依赖
flutter pub get
```

### 4.3 验证安装

```bash
# 检查Flutter环境
flutter doctor

# 列出可用设备
flutter devices
```

### 4.4 运行应用

```bash
# 运行到默认设备
flutter run

# 或指定设备
flutter run -d chrome      # Web
flutter run -d emulator-5554  # Android模拟器
```

---

## 🤖 第5步：ComfyUI部署（3小时）

### 5.1 克隆仓库

```bash
# 创建AI工具目录
mkdir -p ~/ai-tools
cd ~/ai-tools

# 克隆ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### 5.2 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

### 5.3 下载模型

```bash
# 创建模型目录
mkdir -p models/checkpoints

# 下载Stable Diffusion 1.5
# 从 https://huggingface.co/runwayml/stable-diffusion-v1-5 下载
# 或使用以下命令（需要git-lfs）
cd models/checkpoints
# wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
cd ../..

# 注意：模型文件较大（2-7GB），请耐心等待
```

### 5.4 启动ComfyUI

```bash
# 启动服务
python main.py

# 或指定IP和端口
python main.py --listen 0.0.0.0 --port 8188

# 访问Web UI
# http://localhost:8188
```

### 5.5 验证API

```bash
# 在另一个终端测试
curl http://localhost:8188/api/

# 获取系统信息
curl http://localhost:8188/system_stats
```

---

## ✅ 第6步：系统集成测试（1小时）

### 6.1 测试后端连接

```bash
# 在后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 测试数据库连接
python -c "
from app.database import SessionLocal
db = SessionLocal()
result = db.execute('SELECT 1')
print('Database connection OK')
db.close()
"
```

### 6.2 测试ComfyUI连接

```bash
# 测试ComfyUI API
python -c "
import requests
try:
    response = requests.get('http://localhost:8188/api/', timeout=5)
    if response.status_code == 200:
        print('ComfyUI connection OK')
    else:
        print('ComfyUI connection FAILED')
except Exception as e:
    print(f'ComfyUI connection FAILED: {e}')
"
```

### 6.3 启动完整系统

```bash
# 终端1：启动ComfyUI
cd ~/ai-tools/ComfyUI
source venv/bin/activate
python main.py

# 终端2：启动后端
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 终端3：启动前端
cd image_gen_app
flutter run
```

---

## 📊 检查清单

### 后端检查清单
- [ ] 虚拟环境创建完成
- [ ] 依赖安装完成
- [ ] .env文件配置完成
- [ ] 数据库连接测试通过
- [ ] FastAPI应用启动成功
- [ ] API文档可访问（/docs）
- [ ] 健康检查接口正常

### 数据库检查清单
- [ ] PostgreSQL安装完成
- [ ] 数据库创建完成
- [ ] 用户创建完成
- [ ] 初始化脚本执行完成
- [ ] 所有表创建完成
- [ ] 默认数据插入完成
- [ ] 数据库连接测试通过

### 前端检查清单
- [ ] Flutter项目创建完成
- [ ] pubspec.yaml配置完成
- [ ] 依赖安装完成
- [ ] 应用编译成功
- [ ] 应用运行成功

### ComfyUI检查清单
- [ ] 仓库克隆完成
- [ ] 虚拟环境创建完成
- [ ] 依赖安装完成
- [ ] 模型下载完成
- [ ] 服务启动成功
- [ ] Web UI可访问
- [ ] API可调用

---

## 🔧 常见问题解决

### 后端问题

**问题1：数据库连接失败**
```
解决方案：
1. 检查PostgreSQL是否运行
2. 检查.env中的DATABASE_URL是否正确
3. 检查数据库用户和密码是否正确
4. 检查数据库是否存在
```

**问题2：依赖安装失败**
```
解决方案：
1. 升级pip: pip install --upgrade pip
2. 清除缓存: pip cache purge
3. 重新安装: pip install -r requirements.txt
```

**问题3：端口被占用**
```
解决方案：
1. 更改端口: uvicorn app.main:app --port 8001
2. 或杀死占用进程
```

### 前端问题

**问题1：Flutter依赖冲突**
```
解决方案：
1. 清除缓存: flutter clean
2. 获取依赖: flutter pub get
3. 升级依赖: flutter pub upgrade
```

**问题2：编译错误**
```
解决方案：
1. 检查Dart版本: dart --version
2. 检查Flutter版本: flutter --version
3. 运行: flutter doctor
```

### ComfyUI问题

**问题1：模型下载失败**
```
解决方案：
1. 检查网络连接
2. 使用代理或VPN
3. 手动下载模型文件
```

**问题2：CUDA错误**
```
解决方案：
1. 检查GPU驱动
2. 检查CUDA版本
3. 使用CPU模式: python main.py --cpu
```

---

## 📈 进度跟踪

- [ ] 0% - 开始
- [ ] 20% - 后端项目设置完成
- [ ] 40% - 数据库设置完成
- [ ] 60% - 前端项目设置完成
- [ ] 80% - ComfyUI部署完成
- [ ] 100% - 系统集成测试完成

---

## 🎯 完成标志

当以下条件都满足时，第一阶段完成：

✅ 后端项目可运行
✅ 前端项目可编译
✅ 数据库表创建完成
✅ ComfyUI服务运行
✅ 完整系统可启动
✅ 没有编译错误
✅ 没有运行时错误

---

## 📞 获取帮助

- 后端文档：[backend/README.md](backend/README.md)
- 前端文档：[frontend/README.md](frontend/README.md)
- 执行指南：[PHASE1_EXECUTION_GUIDE.md](PHASE1_EXECUTION_GUIDE.md)
- 技术方案：[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)

---

**祝你设置顺利！** 🚀


