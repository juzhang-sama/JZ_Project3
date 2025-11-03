# ImageGen Backend

FastAPI 后端服务

## 快速启动

### 1. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，配置数据库连接等
```

### 4. 初始化数据库

```bash
# 创建PostgreSQL数据库
psql -U postgres -c "CREATE DATABASE image_gen_dev;"

# 创建用户
psql -U postgres -c "CREATE USER image_gen WITH PASSWORD 'your_password';"

# 执行初始化脚本
psql -U image_gen -d image_gen_dev -f init_db.sql
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000

## API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置
│   ├── database.py          # 数据库配置
│   ├── models/              # 数据库模型
│   ├── schemas/             # 数据验证
│   ├── api/                 # API路由
│   ├── services/            # 业务逻辑
│   ├── tasks/               # 异步任务
│   └── utils/               # 工具函数
├── tests/
├── requirements.txt
├── .env.example
├── .gitignore
└── init_db.sql
```

## 开发

### 代码格式化

```bash
black app/
```

### 代码检查

```bash
flake8 app/
```

### 运行测试

```bash
pytest
```

## 部署

### Docker

```bash
docker build -t imagegen-backend .
docker run -p 8000:8000 imagegen-backend
```

## 常见问题

### 数据库连接失败

检查：
1. PostgreSQL是否运行
2. .env中的DATABASE_URL是否正确
3. 数据库用户和密码是否正确

### 端口被占用

```bash
# 更改端口
uvicorn app.main:app --port 8001
```

## 许可证

MIT

