# 第一阶段执行指南 - 基础设施搭建

## 📋 概述

**阶段**：第一阶段（Week 1）
**目标**：完成后端、前端、数据库和ComfyUI的基础设施搭建
**工时**：40小时
**预计时间**：3-4天（连续工作）

---

## 🎯 阶段目标

✅ 后端项目结构完成
✅ 前端项目结构完成
✅ 数据库初始化完成
✅ ComfyUI部署完成
✅ 完整系统可运行

---

## 📅 详细时间表

### 第1天（12小时）

#### 上午（6小时）
- [ ] **1.1** 后端项目初始化（2小时）
  - 创建项目目录结构
  - 创建虚拟环境
  - 安装依赖
  
- [ ] **1.2** 后端配置文件（1小时）
  - 创建.env文件
  - 创建config.py
  - 创建database.py

- [ ] **1.3** 后端基础模型（2小时）
  - 创建User模型
  - 创建GenerationTask模型
  - 创建Result模型
  - 创建Model模型

- [ ] **1.4** 后端主应用（1小时）
  - 创建main.py
  - 配置FastAPI
  - 测试启动

#### 下午（6小时）
- [ ] **1.5** 前端项目初始化（2小时）
  - 创建Flutter项目
  - 创建项目目录结构
  - 配置pubspec.yaml

- [ ] **1.6** 前端配置和模型（2小时）
  - 创建API配置
  - 创建主题配置
  - 创建数据模型

- [ ] **1.7** 前端API服务（1小时）
  - 创建ApiService
  - 配置Dio

- [ ] **1.8** 前端主应用（1小时）
  - 创建main.dart
  - 测试编译和运行

---

### 第2天（14小时）

#### 上午（7小时）
- [ ] **2.1** 数据库初始化（3小时）
  - 创建PostgreSQL数据库
  - 创建用户和权限
  - 创建所有表
  - 插入默认数据

- [ ] **2.2** 数据库验证（1小时）
  - 验证表结构
  - 验证数据
  - 测试连接

- [ ] **2.3** ComfyUI克隆和安装（3小时）
  - 克隆ComfyUI仓库
  - 创建虚拟环境
  - 安装依赖

#### 下午（7小时）
- [ ] **2.4** ComfyUI模型下载（4小时）
  - 下载Stable Diffusion 1.5
  - 下载其他模型（可选）
  - 验证模型文件

- [ ] **2.5** ComfyUI启动和测试（2小时）
  - 启动ComfyUI服务
  - 访问Web UI
  - 测试API

- [ ] **2.6** 后端ComfyUI集成（1小时）
  - 创建ComfyUIService
  - 创建GenerationService
  - 测试集成

---

### 第3天（10小时）

#### 上午（5小时）
- [ ] **3.1** 系统集成测试（3小时）
  - 测试数据库连接
  - 测试ComfyUI连接
  - 测试后端API

- [ ] **3.2** 完整系统启动（2小时）
  - 启动ComfyUI
  - 启动后端
  - 启动前端
  - 验证系统运行

#### 下午（5小时）
- [ ] **3.3** 问题排查和修复（3小时）
  - 修复任何编译错误
  - 修复任何运行时错误
  - 优化配置

- [ ] **3.4** 文档和检查清单（2小时）
  - 完成所有检查清单
  - 记录问题和解决方案
  - 准备第二阶段

---

## 🚀 快速启动命令

### 后端启动
```bash
# 1. 创建项目
mkdir image-gen-backend
cd image-gen-backend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置.env文件
# 编辑.env文件，设置数据库连接等

# 5. 初始化数据库
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# 6. 启动服务
uvicorn app.main:app --reload
```

### 前端启动
```bash
# 1. 创建项目
flutter create image_gen_app
cd image_gen_app

# 2. 获取依赖
flutter pub get

# 3. 运行应用
flutter run
```

### ComfyUI启动
```bash
# 1. 克隆仓库
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python main.py
```

---

## 📊 任务检查清单

### 后端检查清单
- [ ] 项目目录结构创建完成
- [ ] 虚拟环境创建并激活
- [ ] 所有依赖安装完成
- [ ] .env文件配置完成
- [ ] config.py创建完成
- [ ] database.py创建完成
- [ ] 所有模型创建完成
- [ ] main.py创建完成
- [ ] 应用启动成功
- [ ] API文档可访问（/docs）
- [ ] 健康检查接口正常

### 前端检查清单
- [ ] Flutter项目创建完成
- [ ] 项目目录结构创建完成
- [ ] pubspec.yaml配置完成
- [ ] 所有依赖安装完成
- [ ] API配置创建完成
- [ ] 主题配置创建完成
- [ ] 所有模型创建完成
- [ ] ApiService创建完成
- [ ] main.dart创建完成
- [ ] 应用编译成功
- [ ] 应用运行成功

### 数据库检查清单
- [ ] PostgreSQL安装完成
- [ ] 数据库创建完成
- [ ] 用户创建完成
- [ ] 权限配置完成
- [ ] 所有表创建完成
- [ ] 索引创建完成
- [ ] 默认数据插入完成
- [ ] 数据库连接测试通过
- [ ] 表结构验证完成

### ComfyUI检查清单
- [ ] 仓库克隆完成
- [ ] 虚拟环境创建完成
- [ ] 依赖安装完成
- [ ] 模型下载完成
- [ ] 服务启动成功
- [ ] Web UI可访问
- [ ] API可调用
- [ ] 健康检查通过

### 集成检查清单
- [ ] 后端可连接数据库
- [ ] 后端可连接ComfyUI
- [ ] 前端可连接后端
- [ ] 完整系统可运行
- [ ] 没有编译错误
- [ ] 没有运行时错误

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
2. 或杀死占用进程: lsof -i :8000 | kill -9
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

### 第1天进度
- [ ] 0% - 开始
- [ ] 25% - 后端项目初始化完成
- [ ] 50% - 后端配置完成
- [ ] 75% - 前端项目初始化完成
- [ ] 100% - 前端配置完成

### 第2天进度
- [ ] 0% - 开始
- [ ] 25% - 数据库初始化完成
- [ ] 50% - ComfyUI安装完成
- [ ] 75% - 模型下载完成
- [ ] 100% - ComfyUI启动成功

### 第3天进度
- [ ] 0% - 开始
- [ ] 50% - 系统集成测试完成
- [ ] 75% - 问题修复完成
- [ ] 100% - 第一阶段完成

---

## 🎉 完成标志

当以下条件都满足时，第一阶段完成：

✅ 后端项目可运行
✅ 前端项目可编译
✅ 数据库表创建完成
✅ ComfyUI服务运行
✅ 完整系统可启动
✅ 没有编译错误
✅ 没有运行时错误
✅ 所有检查清单完成

---

## 📝 下一步

完成第一阶段后，进入第二阶段：

**第二阶段：认证系统实现**
- 用户注册接口
- 用户登录接口
- JWT认证
- 路由保护
- 前端认证UI

预计时间：第2周（35小时）

---

## 📞 获取帮助

如遇到问题，请参考：
1. [PHASE1_BACKEND_SETUP.md](PHASE1_BACKEND_SETUP.md)
2. [PHASE1_FRONTEND_SETUP.md](PHASE1_FRONTEND_SETUP.md)
3. [PHASE1_DATABASE_COMFYUI_SETUP.md](PHASE1_DATABASE_COMFYUI_SETUP.md)
4. [MVP_TECH_PLAN.md](MVP_TECH_PLAN.md)

---

**祝你开发顺利！** 🚀


