# 极简MVP前期准备清单

## ✅ 开发环境准备

### 必需工具安装

#### Flutter开发环境
- [ ] 下载Flutter SDK 3.x
  - 官网：https://flutter.dev/docs/get-started/install
  - 版本：3.13+
- [ ] 配置Flutter环境变量
  ```bash
  flutter --version
  flutter doctor
  ```
- [ ] 安装Android开发工具
  - Android SDK
  - Android Studio
  - 模拟器或真机
- [ ] 安装iOS开发工具（Mac用户）
  - Xcode
  - CocoaPods
  - iOS模拟器或真机

#### Python开发环境
- [ ] 安装Python 3.10+
  - 官网：https://www.python.org/
  - 验证：`python --version`
- [ ] 安装pip包管理器
  - 验证：`pip --version`
- [ ] 创建虚拟环境工具
  - `python -m venv`

#### 数据库和缓存
- [ ] 安装PostgreSQL 14+
  - 官网：https://www.postgresql.org/
  - 创建数据库用户
  - 创建开发数据库
- [ ] 安装Redis 7.x
  - 官网：https://redis.io/
  - 验证：`redis-cli ping`

#### 版本控制
- [ ] 安装Git
  - 官网：https://git-scm.com/
  - 配置用户名和邮箱
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your@email.com"
  ```

#### 代码编辑器
- [ ] 安装VS Code
  - 官网：https://code.visualstudio.com/
  - 安装Flutter扩展
  - 安装Python扩展
  - 安装Dart扩展
  - 安装REST Client扩展

---

## 🔧 后端环境配置

### Python项目初始化
- [ ] 创建项目目录
  ```bash
  mkdir image-gen-backend
  cd image-gen-backend
  ```
- [ ] 创建虚拟环境
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  ```
- [ ] 创建requirements.txt
  ```
  fastapi==0.104.1
  uvicorn==0.24.0
  sqlalchemy==2.0.23
  psycopg2-binary==2.9.9
  pydantic==2.5.0
  pydantic-settings==2.1.0
  python-jose==3.3.0
  passlib==1.7.4
  python-multipart==0.0.6
  celery==5.3.4
  redis==5.0.1
  requests==2.31.0
  python-dotenv==1.0.0
  alembic==1.13.0
  ```
- [ ] 安装依赖
  ```bash
  pip install -r requirements.txt
  ```

### 数据库配置
- [ ] 创建PostgreSQL数据库
  ```sql
  CREATE DATABASE image_gen_dev;
  CREATE USER image_gen WITH PASSWORD 'your_password';
  ALTER ROLE image_gen SET client_encoding TO 'utf8';
  ALTER ROLE image_gen SET default_transaction_isolation TO 'read committed';
  ALTER ROLE image_gen SET default_transaction_deferrable TO on;
  GRANT ALL PRIVILEGES ON DATABASE image_gen_dev TO image_gen;
  ```
- [ ] 配置数据库连接字符串
  ```
  DATABASE_URL=postgresql://image_gen:password@localhost:5432/image_gen_dev
  ```

### Redis配置
- [ ] 启动Redis服务
  ```bash
  redis-server
  ```
- [ ] 验证Redis连接
  ```bash
  redis-cli ping
  ```
- [ ] 配置Redis连接字符串
  ```
  REDIS_URL=redis://localhost:6379/0
  ```

### 环境变量配置
- [ ] 创建.env文件
  ```
  # Database
  DATABASE_URL=postgresql://image_gen:password@localhost:5432/image_gen_dev
  
  # Redis
  REDIS_URL=redis://localhost:6379/0
  
  # JWT
  SECRET_KEY=your-secret-key-here-change-in-production
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  
  # ComfyUI
  COMFYUI_URL=http://localhost:8188
  
  # API
  API_HOST=0.0.0.0
  API_PORT=8000
  
  # Environment
  ENVIRONMENT=development
  ```

---

## 🎨 前端环境配置

### Flutter项目初始化
- [ ] 创建Flutter项目
  ```bash
  flutter create image_gen_app
  cd image_gen_app
  ```
- [ ] 配置pubspec.yaml依赖
  ```yaml
  dependencies:
    flutter:
      sdk: flutter
    dio: ^5.3.0
    provider: ^6.0.0
    go_router: ^11.0.0
    hive: ^2.2.0
    hive_flutter: ^1.1.0
    cached_network_image: ^3.3.0
    image_picker: ^1.0.0
    share_plus: ^7.0.0
    intl: ^0.19.0
  
  dev_dependencies:
    flutter_test:
      sdk: flutter
    flutter_lints: ^2.0.0
  ```
- [ ] 获取依赖
  ```bash
  flutter pub get
  ```

### 项目结构创建
- [ ] 创建目录结构
  ```
  lib/
  ├── screens/
  ├── providers/
  ├── services/
  ├── models/
  ├── widgets/
  ├── utils/
  ├── config/
  └── main.dart
  ```

### 配置文件
- [ ] 创建API配置文件
  ```dart
  // lib/config/api_config.dart
  const String API_BASE_URL = 'http://localhost:8000/api/v1';
  const int API_TIMEOUT = 30000; // 30秒
  ```

---

## 🤖 ComfyUI环境配置

### ComfyUI部署
- [ ] 克隆ComfyUI仓库
  ```bash
  git clone https://github.com/comfyanonymous/ComfyUI.git
  cd ComfyUI
  ```
- [ ] 安装Python依赖
  ```bash
  pip install -r requirements.txt
  ```
- [ ] 下载基础模型
  - Stable Diffusion 1.5
  - Stable Diffusion XL
  - 其他必需模型
  - 放在 `models/checkpoints/` 目录

### ComfyUI配置
- [ ] 启动ComfyUI
  ```bash
  python main.py
  ```
- [ ] 验证API可用
  ```bash
  curl http://localhost:8188/api/
  ```
- [ ] 配置API端口
  - 默认：8188
  - 可在启动时指定：`python main.py --listen 0.0.0.0 --port 8188`

### 工作流准备
- [ ] 创建基础文本转图像工作流
  - 输入：提示词
  - 模型：Stable Diffusion
  - 输出：图片
- [ ] 测试工作流
  - 通过ComfyUI Web UI测试
  - 导出工作流JSON

---

## ☁️ 云服务配置（可选）

### 云服务器选择
- [ ] 选择云服务商
  - 阿里云
  - 腾讯云
  - 其他
- [ ] 创建账号并实名认证

### 云服务器配置
- [ ] 购买ECS实例
  - 配置：2核4GB（最低）
  - 系统：Ubuntu 20.04 LTS
  - 存储：50GB
- [ ] 配置安全组
  - 开放端口：22（SSH）、80（HTTP）、443（HTTPS）、8000（API）
- [ ] 配置密钥对
  - 下载私钥
  - 配置SSH连接

### 云数据库配置
- [ ] 购买RDS PostgreSQL
  - 版本：14+
  - 存储：20GB
- [ ] 购买Redis缓存
  - 版本：7.x
  - 容量：1GB

### 对象存储配置
- [ ] 创建OSS/COS Bucket
  - 名称：image-gen-results
  - 访问权限：私有
  - 配置CORS

---

## 🔐 安全配置

### JWT密钥生成
- [ ] 生成安全的JWT密钥
  ```python
  import secrets
  print(secrets.token_urlsafe(32))
  ```
- [ ] 保存到.env文件

### 数据库密码
- [ ] 生成强密码
  ```bash
  openssl rand -base64 32
  ```
- [ ] 保存到.env文件

### HTTPS证书（生产环境）
- [ ] 申请SSL证书
  - Let's Encrypt（免费）
  - 商业证书
- [ ] 配置Nginx反向代理

---

## 📦 代码仓库配置

### Git仓库初始化
- [ ] 创建GitHub/GitLab仓库
- [ ] 克隆到本地
  ```bash
  git clone <repository-url>
  ```
- [ ] 创建.gitignore文件
  ```
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  venv/
  .env
  
  # Flutter
  build/
  .dart_tool/
  .flutter-plugins
  
  # IDE
  .vscode/
  .idea/
  *.swp
  
  # OS
  .DS_Store
  Thumbs.db
  ```

### 分支策略
- [ ] 创建主分支
  - main（生产）
  - develop（开发）
- [ ] 配置分支保护规则
  - 需要代码审查
  - 需要通过CI/CD

---

## 📋 项目初始化检查清单

### 后端检查
- [ ] FastAPI项目可运行
  ```bash
  uvicorn app.main:app --reload
  ```
- [ ] 数据库连接正常
  ```bash
  python -c "from app.database import engine; engine.connect()"
  ```
- [ ] Redis连接正常
  ```bash
  redis-cli ping
  ```
- [ ] Celery可运行
  ```bash
  celery -A app.tasks worker --loglevel=info
  ```

### 前端检查
- [ ] Flutter项目可编译
  ```bash
  flutter build apk --debug
  ```
- [ ] 模拟器/真机可运行
  ```bash
  flutter run
  ```

### ComfyUI检查
- [ ] ComfyUI Web UI可访问
  - http://localhost:8188
- [ ] API可调用
  - http://localhost:8188/api/

### 集成检查
- [ ] 前端可连接后端API
- [ ] 后端可调用ComfyUI
- [ ] 数据库可正常读写

---

## 🚀 快速启动脚本

### 后端启动脚本（start_backend.sh）
```bash
#!/bin/bash
source venv/bin/activate
export $(cat .env | xargs)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动脚本（start_frontend.sh）
```bash
#!/bin/bash
flutter run
```

### ComfyUI启动脚本（start_comfyui.sh）
```bash
#!/bin/bash
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### 完整启动脚本（start_all.sh）
```bash
#!/bin/bash
# 启动Redis
redis-server &

# 启动ComfyUI
cd ComfyUI && python main.py &

# 启动后端
cd ../backend && source venv/bin/activate && uvicorn app.main:app --reload &

# 启动前端
cd ../frontend && flutter run
```

---

## 📝 总结

完成以上准备工作后，你将拥有：

✅ 完整的开发环境
✅ 配置好的数据库和缓存
✅ 可运行的ComfyUI
✅ 初始化的前后端项目
✅ 配置好的代码仓库

**下一步**：开始第一阶段的基础设施搭建。


