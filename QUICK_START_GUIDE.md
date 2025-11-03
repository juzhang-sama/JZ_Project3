# 极简MVP快速启动指南

## 📚 文档导航

### 核心文档
1. **[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)** - 技术方案详解
   - 技术栈选择
   - 系统架构设计
   - 数据库设计
   - API接口设计

2. **[MVP_DEVELOPMENT_PLAN.md](MVP_DEVELOPMENT_PLAN.md)** - 开发计划详解
   - 7个开发阶段
   - 详细任务清单
   - 工时分配
   - 关键里程碑

3. **[MVP_PREPARATION_CHECKLIST.md](MVP_PREPARATION_CHECKLIST.md)** - 前期准备清单
   - 开发环境安装
   - 数据库配置
   - ComfyUI部署
   - 代码仓库设置

4. **[MVP_PROJECT_SUMMARY.md](MVP_PROJECT_SUMMARY.md)** - 项目总结
   - 项目概述
   - 功能定义
   - 成本估算
   - 后期迭代方向

---

## 🚀 5分钟快速了解

### 项目是什么？
一个**极简AI图像生成应用**，用户通过简单的界面：
1. 输入提示词
2. 选择模型
3. 点击生成
4. 查看结果

### 技术栈是什么？
```
前端：Flutter 3.x（跨平台移动应用）
后端：FastAPI + Python（高性能API）
数据库：PostgreSQL + Redis（数据存储和缓存）
AI引擎：ComfyUI（图像生成）
```

### 需要多长时间？
**4-6周**（125小时工作量）

### 需要多少钱？
**月运营成本：100-200元**（云服务器、数据库、存储）

### 核心功能有哪些？
- ✅ 用户认证（注册/登录）
- ✅ 提示词输入
- ✅ 模型选择（3-5个基础模型）
- ✅ 图片生成
- ✅ 结果展示
- ✅ 历史记录
- ✅ 下载分享

---

## 📋 前期准备（1-2天）

### 第一步：安装开发工具
```bash
# 1. 安装Flutter
# 下载：https://flutter.dev/docs/get-started/install
flutter --version

# 2. 安装Python
# 下载：https://www.python.org/
python --version

# 3. 安装PostgreSQL
# 下载：https://www.postgresql.org/
psql --version

# 4. 安装Redis
# 下载：https://redis.io/
redis-cli --version

# 5. 安装Git
# 下载：https://git-scm.com/
git --version
```

### 第二步：配置数据库
```bash
# 创建PostgreSQL数据库
psql -U postgres
CREATE DATABASE image_gen_dev;
CREATE USER image_gen WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE image_gen_dev TO image_gen;
```

### 第三步：部署ComfyUI
```bash
# 克隆ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 安装依赖
pip install -r requirements.txt

# 下载模型
# 将模型放在 models/checkpoints/ 目录

# 启动ComfyUI
python main.py
```

### 第四步：创建代码仓库
```bash
# 创建项目目录
mkdir image-gen
cd image-gen

# 初始化Git
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

---

## 🏗️ 开发流程（4-6周）

### 第1周：基础设施搭建
```bash
# 后端
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis celery

# 前端
flutter create frontend
cd frontend
flutter pub get
```

### 第2周：认证和生成功能
- 实现用户注册/登录
- 实现提示词输入
- 实现模型选择
- 实现生成功能

### 第3周：结果管理
- 实现历史记录
- 实现下载功能
- 实现分享功能

### 第4周：优化和测试
- UI/UX优化
- 功能测试
- 性能优化

### 第5周：部署发布
- 生产环境部署
- 应用发布

---

## 🔌 核心API接口

### 认证
```
POST /api/v1/auth/register
  请求：{username, email, password}
  响应：{user_id, token}

POST /api/v1/auth/login
  请求：{email, password}
  响应：{user_id, token}
```

### 生成
```
POST /api/v1/generation/generate
  请求：{prompt, model_name}
  响应：{task_id, status}

GET /api/v1/generation/tasks/{task_id}
  响应：{task_id, status, result_url}

GET /api/v1/generation/history
  响应：[{task_id, prompt, model, status, created_at}]
```

### 模型
```
GET /api/v1/models
  响应：[{id, name, display_name, description}]
```

---

## 📊 数据库表

### users 表
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### generation_tasks 表
```sql
CREATE TABLE generation_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    prompt TEXT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    result_id INTEGER REFERENCES results(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### results 表
```sql
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES generation_tasks(id),
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 关键里程碑

| 时间 | 里程碑 | 完成度 |
|------|--------|--------|
| 第1周 | 基础设施完成 | 20% |
| 第2周初 | 认证系统完成 | 40% |
| 第2周末 | 核心功能完成 | 70% |
| 第3周 | 结果管理完成 | 85% |
| 第4周初 | UI优化完成 | 90% |
| 第4周末 | 测试优化完成 | 95% |
| 第5周 | 部署发布完成 | 100% |

---

## 💡 开发建议

### 1. 从简单开始
- 先实现基础功能
- 再逐步添加优化
- 不要过度设计

### 2. 频繁测试
- 每天测试一次
- 及时发现问题
- 快速迭代修复

### 3. 保持代码质量
- 遵循代码规范
- 编写清晰的注释
- 定期重构

### 4. 文档很重要
- 记录设计决策
- 编写API文档
- 编写部署指南

### 5. 备份很重要
- 定期提交Git
- 备份数据库
- 备份配置文件

---

## 🔧 常用命令

### 后端命令
```bash
# 启动开发服务器
uvicorn app.main:app --reload

# 运行数据库迁移
alembic upgrade head

# 启动Celery Worker
celery -A app.tasks worker --loglevel=info

# 运行测试
pytest
```

### 前端命令
```bash
# 运行应用
flutter run

# 构建APK
flutter build apk

# 构建iOS
flutter build ios

# 清理构建
flutter clean
```

### 数据库命令
```bash
# 连接数据库
psql -U image_gen -d image_gen_dev

# 查看表
\dt

# 查看表结构
\d table_name
```

---

## 🐛 常见问题

### Q: 如何处理长时间的生成任务？
A: 使用Celery异步任务队列，前端轮询查询任务状态。

### Q: 如何存储生成的图片？
A: 保存到本地文件系统或对象存储（OSS/COS）。

### Q: 如何处理并发请求？
A: 使用Redis缓存和数据库连接池。

### Q: 如何部署到生产环境？
A: 使用Docker容器化，部署到云服务器。

### Q: 如何监控应用状态？
A: 配置日志系统和监控告警。

---

## 📞 获取帮助

### 官方文档
- Flutter: https://flutter.dev/docs
- FastAPI: https://fastapi.tiangolo.com/
- ComfyUI: https://github.com/comfyanonymous/ComfyUI
- PostgreSQL: https://www.postgresql.org/docs/

### 社区资源
- Flutter社区：https://flutter.dev/community
- FastAPI讨论：https://github.com/tiangolo/fastapi/discussions
- ComfyUI讨论：https://github.com/comfyanonymous/ComfyUI/discussions

---

## ✅ 检查清单

开始开发前，确保：
- [ ] 所有开发工具已安装
- [ ] 数据库已配置
- [ ] ComfyUI已部署
- [ ] Git仓库已创建
- [ ] 环境变量已配置
- [ ] 所有文档已阅读

---

## 🎉 准备好开始了吗？

1. ✅ 完成前期准备
2. ✅ 阅读技术方案
3. ✅ 按照开发计划执行
4. ✅ 定期测试和优化
5. ✅ 部署和发布

**祝你开发顺利！** 🚀


