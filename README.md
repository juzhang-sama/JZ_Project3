# 极简MVP项目 - 对标RunningHub

## 📱 项目概述

这是一个**极简AI图像生成应用**的完整技术方案和开发计划。

**核心功能**：用户输入提示词 → 选择模型 → 后台调用ComfyUI生成图片 → 返回并展示结果

**开发周期**：4-6周
**开发成本**：极低（单人开发可行）
**月运营成本**：100-200元

---

## 🎯 项目特点

### ✨ 极简设计
- 只做核心功能闭环
- 不做复杂工作流编辑
- 不做节点市场
- 不做高级控制（ControlNet/LoRA）

### 🚀 快速开发
- 4-6周完成MVP
- 125小时工作量
- 单人开发可行
- 成熟技术栈

### 💰 成本优化
- 开源技术栈
- 最小化云服务依赖
- 可本地部署
- 月运营成本100-200元

### 📈 易于扩展
- 为后期功能迭代预留接口
- 清晰的模块划分
- 完整的文档体系

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端** | Flutter 3.x | 跨平台移动应用 |
| | Dart | 编程语言 |
| | Provider | 状态管理 |
| **后端** | FastAPI | 高性能API框架 |
| | Python 3.10+ | 编程语言 |
| | SQLAlchemy | ORM框架 |
| **数据库** | PostgreSQL | 主数据库 |
| | Redis | 缓存和任务队列 |
| **任务处理** | Celery | 异步任务队列 |
| **AI引擎** | ComfyUI | 图像生成引擎 |
| **部署** | Docker | 容器化 |

---

## 📚 文档清单

### 核心文档
1. **[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)** ⭐ 必读
   - 技术栈详解
   - 系统架构设计
   - 数据库设计
   - API接口设计

2. **[MVP_DEVELOPMENT_PLAN.md](MVP_DEVELOPMENT_PLAN.md)** ⭐ 必读
   - 7个开发阶段
   - 详细任务清单
   - 工时分配
   - 关键里程碑

3. **[MVP_PREPARATION_CHECKLIST.md](MVP_PREPARATION_CHECKLIST.md)** ⭐ 必读
   - 开发环境安装
   - 数据库配置
   - ComfyUI部署
   - 代码仓库设置

4. **[MVP_PROJECT_SUMMARY.md](MVP_PROJECT_SUMMARY.md)**
   - 项目总结
   - 功能定义
   - 成本估算
   - 后期迭代方向

5. **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)**
   - 快速启动指南
   - 常用命令
   - 常见问题
   - 获取帮助

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────┐
│     前端 (Flutter)                  │
│  提示词输入 → 模型选择 → 结果展示   │
└────────────────┬────────────────────┘
                 │ REST API
┌────────────────▼────────────────────┐
│     后端 (FastAPI)                  │
│  认证 | 生成 | 结果 | 历史          │
└────────────────┬────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│PostgreSQL│ │ Redis  │  │ComfyUI   │
│ 数据库   │ │ 缓存   │  │ 执行引擎 │
└────────┘  └────────┘  └──────────┘
```

---

## 🎯 核心功能

### MVP必做功能
```
✅ 用户认证系统
   - 注册/登录
   - 基础用户信息管理

✅ 提示词输入
   - 简单文本输入框
   - 基础提示词建议

✅ 模型选择
   - 预设3-5个基础模型
   - 模型快速切换

✅ 图片生成
   - 调用ComfyUI后端
   - 实时进度反馈
   - 生成结果展示

✅ 结果管理
   - 生成历史记录
   - 图片下载
   - 基础分享功能
```

---

## 📅 开发计划

### 第1周：基础设施搭建（40小时）
- 后端项目初始化
- 前端项目初始化
- 数据库配置
- ComfyUI部署

### 第2周：认证和生成（35小时）
- 认证系统实现
- 生成功能实现
- 前端界面开发

### 第3周：结果管理（20小时）
- 结果管理功能
- 历史记录功能
- 下载分享功能

### 第4周：优化和测试（20小时）
- UI/UX优化
- 功能测试
- 性能优化

### 第5周：部署发布（15小时）
- 生产环境部署
- 应用发布
- 文档编写

**总计**：125小时（4-6周）

---

## 🚀 快速启动

### 1. 前期准备（1-2天）
```bash
# 安装开发工具
# - Flutter SDK 3.x
# - Python 3.10+
# - PostgreSQL 14+
# - Redis 7.x
# - Git

# 配置数据库
# - 创建PostgreSQL数据库
# - 启动Redis服务

# 部署ComfyUI
# - 克隆ComfyUI仓库
# - 安装依赖
# - 下载模型
# - 启动服务
```

### 2. 后端启动
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. 前端启动
```bash
flutter pub get
flutter run
```

### 4. ComfyUI启动
```bash
cd ComfyUI
python main.py
```

---

## 💰 成本估算

### 开发成本
```
前端开发：50小时
后端开发：40小时
基础设施：15小时
测试优化：20小时
─────────────────
总计：125小时
```

### 运营成本（月）
```
云服务器：50-100元
数据库：30-50元
存储：10-20元
带宽：20-50元
─────────────────
总计：110-220元/月
```

---

## 📋 前期准备清单

### 必需工具
- [ ] Flutter SDK 3.x
- [ ] Python 3.10+
- [ ] PostgreSQL 14+
- [ ] Redis 7.x
- [ ] Git
- [ ] VS Code

### 第三方服务
- [ ] ComfyUI部署
- [ ] 云服务器账号（可选）

### 代码仓库
- [ ] 创建Git仓库
- [ ] 配置.gitignore
- [ ] 创建分支策略

详见：[MVP_PREPARATION_CHECKLIST.md](MVP_PREPARATION_CHECKLIST.md)

---

## 🔌 核心API接口

### 认证
```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

### 生成
```
POST /api/v1/generation/generate
GET /api/v1/generation/tasks/{task_id}
GET /api/v1/generation/history
```

### 模型
```
GET /api/v1/models
```

### 结果
```
GET /api/v1/results/{result_id}
DELETE /api/v1/results/{result_id}
```

详见：[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)

---

## 📊 数据库设计

### 核心表
- **users** - 用户信息
- **generation_tasks** - 生成任务
- **results** - 生成结果
- **models** - 模型配置

详见：[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)

---

## ✨ 技术亮点

### 1. 极简架构
- 最小化功能集合
- 快速迭代
- 易于维护

### 2. 异步处理
- Celery任务队列
- 不阻塞用户请求
- 支持长时间运行的生成任务

### 3. 跨平台支持
- Flutter支持iOS/Android
- 一套代码多平台运行

### 4. 高效开发
- FastAPI自动文档
- 热重载支持
- 快速原型开发

### 5. 成本优化
- 开源技术栈
- 最小化云服务依赖
- 可本地部署

---

## 🔮 后期迭代方向

### Phase 2（第6-8周）
- 复杂工作流编辑
- 高级参数控制
- 模型管理界面

### Phase 3（第9-12周）
- 创作者经济
- 工作流分享
- 社区功能

### Phase 4（第13+周）
- ControlNet/LoRA支持
- 模型训练
- 实时协作

---

## 📞 获取帮助

### 官方文档
- Flutter: https://flutter.dev/docs
- FastAPI: https://fastapi.tiangolo.com/
- ComfyUI: https://github.com/comfyanonymous/ComfyUI
- PostgreSQL: https://www.postgresql.org/docs/

### 常见问题
详见：[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

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

1. ✅ 阅读本README
2. ✅ 阅读[MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)
3. ✅ 完成[MVP_PREPARATION_CHECKLIST.md](MVP_PREPARATION_CHECKLIST.md)
4. ✅ 按照[MVP_DEVELOPMENT_PLAN.md](MVP_DEVELOPMENT_PLAN.md)执行
5. ✅ 参考[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

**祝你开发顺利！** 🚀

---

## 📝 项目状态

- ✅ 技术方案完成
- ✅ 开发计划完成
- ✅ 前期准备清单完成
- ⏳ 等待开始开发

**预计上线时间**：4-6周后

---

## 📄 许可证

MIT License

---

**最后更新**：2025年1月
**版本**：1.0


