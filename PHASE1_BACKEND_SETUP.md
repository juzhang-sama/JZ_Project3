# 第一阶段：后端项目初始化

## 📋 任务概述

**目标**：创建FastAPI项目结构，配置所有依赖，初始化数据库
**时间**：第1-2天（20小时）
**完成标志**：后端API框架可运行，数据库表创建完成

---

## 🚀 第一步：创建项目结构

### 1.1 创建项目目录
```bash
# 创建项目根目录
mkdir image-gen-backend
cd image-gen-backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 1.2 创建项目目录结构
```bash
mkdir -p app/{api,models,schemas,services,tasks,utils}
mkdir -p tests
mkdir -p logs
touch app/__init__.py
touch app/main.py
touch app/config.py
touch app/database.py
touch .env
touch .gitignore
touch requirements.txt
```

### 1.3 最终项目结构
```
image-gen-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置文件
│   ├── database.py             # 数据库配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py             # 认证接口
│   │   ├── users.py            # 用户接口
│   │   ├── generation.py       # 生成接口
│   │   └── results.py          # 结果接口
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   ├── generation_task.py  # 生成任务模型
│   │   └── result.py           # 结果模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # 用户schema
│   │   ├── generation.py       # 生成schema
│   │   └── result.py           # 结果schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # 认证服务
│   │   ├── generation_service.py # 生成服务
│   │   ├── comfyui_service.py  # ComfyUI服务
│   │   └── storage_service.py  # 存储服务
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── celery_tasks.py     # Celery任务
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # 安全工具
│       └── validators.py       # 验证工具
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_generation.py
├── logs/
├── venv/
├── .env                        # 环境变量
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📦 第二步：配置依赖

### 2.1 创建requirements.txt
```
# Web框架
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.0

# 数据验证
pydantic==2.5.0
pydantic-settings==2.1.0

# 认证
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1

# 异步任务
celery==5.3.4
redis==5.0.1

# HTTP客户端
requests==2.31.0
httpx==0.25.2

# 环境变量
python-dotenv==1.0.0

# 日志
python-json-logger==2.0.7

# 开发工具
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
flake8==6.1.0
```

### 2.2 安装依赖
```bash
pip install -r requirements.txt
```

---

## 🔧 第三步：配置文件

### 3.1 创建.env文件
```
# 数据库配置
DATABASE_URL=postgresql://image_gen:password@localhost:5432/image_gen_dev

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ComfyUI配置
COMFYUI_URL=http://localhost:8188
COMFYUI_TIMEOUT=300

# API配置
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=ImageGen API
API_VERSION=0.1.0

# 环境
ENVIRONMENT=development
DEBUG=True

# 日志
LOG_LEVEL=INFO
```

### 3.2 创建.gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Testing
.pytest_cache/
.coverage
htmlcov/

# Celery
celerybeat-schedule
```

---

## 🗄️ 第四步：数据库配置

### 4.1 创建PostgreSQL数据库
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
GRANT ALL PRIVILEGES ON DATABASE image_gen_dev TO image_gen;

# 退出
\q
```

### 4.2 创建app/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://image_gen:password@localhost:5432/image_gen_dev")

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=os.getenv("DEBUG", False)
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.3 创建app/config.py
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API配置
    API_TITLE: str = "ImageGen API"
    API_VERSION: str = "0.1.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 数据库
    DATABASE_URL: str = "postgresql://image_gen:password@localhost:5432/image_gen_dev"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ComfyUI
    COMFYUI_URL: str = "http://localhost:8188"
    COMFYUI_TIMEOUT: int = 300
    
    # 环境
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## 🏗️ 第五步：创建基础模型

### 5.1 创建app/models/user.py
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### 5.2 创建app/models/generation_task.py
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class GenerationTask(Base):
    __tablename__ = "generation_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    result_id = Column(Integer, ForeignKey("results.id"), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
```

### 5.3 创建app/models/result.py
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("generation_tasks.id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    image_path = Column(String(255), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

## 📝 第六步：创建基础API

### 6.1 创建app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
import logging

# 创建所有表
Base.metadata.create_all(bind=engine)

# 创建应用
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日志
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 根路由
@app.get("/")
async def root():
    return {
        "message": "ImageGen API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
```

### 6.2 创建app/api/__init__.py
```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# 这里将导入所有路由
# from app.api import auth, users, generation, results
# router.include_router(auth.router)
# router.include_router(users.router)
# router.include_router(generation.router)
# router.include_router(results.router)
```

---

## ✅ 第七步：验证安装

### 7.1 测试数据库连接
```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 测试导入
python -c "from app.database import engine; print('Database connection OK')"
```

### 7.2 启动开发服务器
```bash
# 启动FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7.3 验证API
```bash
# 在另一个终端测试
curl http://localhost:8000/health
curl http://localhost:8000/

# 访问API文档
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

---

## 📊 检查清单

完成以下检查：
- [ ] 项目目录结构创建完成
- [ ] 虚拟环境创建并激活
- [ ] 所有依赖安装完成
- [ ] .env文件配置完成
- [ ] PostgreSQL数据库创建完成
- [ ] 数据库连接测试通过
- [ ] 基础模型创建完成
- [ ] FastAPI应用启动成功
- [ ] API文档可访问（/docs）
- [ ] 健康检查接口正常

---

## 🎯 完成标志

✅ 后端项目结构完成
✅ 所有依赖安装完成
✅ 数据库配置完成
✅ FastAPI应用可运行
✅ API文档可访问

**下一步**：创建前端项目初始化


