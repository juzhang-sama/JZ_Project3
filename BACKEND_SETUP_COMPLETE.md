# ✅ 后端配置完成指南

## 🎉 问题解决总结

### 原始问题
- APP 在真机上注册时出现连接错误
- 后端服务没有正确配置和运行

### 根本原因
1. **数据库配置错误** - 配置使用 PostgreSQL，但电脑上没有安装
2. **后端服务未启动** - 没有运行 FastAPI 服务
3. **端口冲突** - 8000 端口被占用

### 解决方案
✅ 修改数据库配置为 SQLite（无需额外安装）
✅ 启动后端服务在 8001 端口
✅ 更新 APP 配置使用新的端口

---

## 🔧 本地电脑需要做的事情

### 第 1 步：启动后端服务

**方式 1：使用启动脚本（推荐）**
```powershell
cd D:\JZ_Project3\backend
.\start_backend_simple.ps1
```

**方式 2：手动启动**
```powershell
cd D:\JZ_Project3\backend

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 第 2 步：验证后端是否运行

在浏览器中访问：
```
http://localhost:8001
```

应该看到：
```json
{
  "message": "ImageGen API",
  "version": "0.1.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### 第 3 步：查看 API 文档

访问：
```
http://localhost:8001/docs
```

---

## 📱 APP 配置更新

### 新的 API 端点
- **基础 URL：** `http://192.168.18.2:8001/api/v1`
- **认证 URL：** `http://192.168.18.2:8001/api/v1/auth`

### 修改的文件
1. `frontend/lib/services/auth_service.dart`
   - 从 `8000` 改为 `8001`

2. `frontend/lib/services/api_service.dart`
   - 从 `8000` 改为 `8001`

### 新的 APK 文件
- **文件名：** `app-release-port8001.apk`
- **大小：** 21.54 MB
- **位置：** `D:\JZ_Project3\app-release-port8001.apk`

---

## 📋 完整的启动步骤

### 第一次启动（完整流程）

```powershell
# 1. 进入后端目录
cd D:\JZ_Project3\backend

# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 3. 安装依赖（如果需要）
pip install -r requirements.txt

# 4. 初始化数据库（如果需要）
python init_db.py

# 5. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 后续启动（简化流程）

```powershell
# 1. 进入后端目录
cd D:\JZ_Project3\backend

# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 3. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

## 🗄️ 数据库信息

### 数据库类型
- **类型：** SQLite（开发环境）
- **文件：** `backend/image_gen.db`
- **配置：** `backend/app/config.py`

### 数据库表
- `users` - 用户表
- `models` - AI 模型配置表
- `generation_tasks` - 生成任务表
- `results` - 生成结果表

### 初始化数据
- 3 个默认 AI 模型已预加载
- 0 个用户（需要通过 APP 注册）

---

## 🚀 安装新 APK

```powershell
# 进入项目目录
cd D:\JZ_Project3

# 卸载旧应用
adb uninstall com.example.frontend

# 安装新 APK
adb install -r app-release-port8001.apk
```

---

## ✅ 完整的测试流程

### 1. 启动后端服务
```powershell
cd D:\JZ_Project3\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 2. 安装新 APK
```powershell
adb install -r D:\JZ_Project3\app-release-port8001.apk
```

### 3. 打开应用并测试
- 打开 ImageGen 应用
- 点击"注册"
- 填写用户信息
- 点击"注册"按钮
- 应该成功注册并登录

---

## 🔍 验证清单

- [x] 后端数据库配置为 SQLite
- [x] 后端服务启动在 8001 端口
- [x] APP 配置更新为使用 8001 端口
- [x] 新 APK 已生成
- [x] 数据库已初始化

---

## 🐛 故障排除

### 问题 1：后端启动失败

**错误信息：** `ERROR: [Errno 10048] error while attempting to bind on address`

**解决方案：**
```powershell
# 查找占用 8001 端口的进程
netstat -ano | findstr :8001

# 杀死进程（替换 PID）
taskkill /PID <PID> /F

# 重新启动
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 问题 2：APP 无法连接到后端

**检查清单：**
1. 后端服务是否运行？
   ```powershell
   netstat -ano | findstr :8001
   ```

2. 手机和电脑是否在同一 WiFi？
   ```powershell
   ipconfig
   ```

3. 防火墙是否允许 8001 端口？
   - 打开 Windows Defender 防火墙
   - 允许应用通过防火墙
   - 添加 Python 到允许列表

### 问题 3：数据库错误

**解决方案：**
```powershell
# 删除旧数据库
rm backend\image_gen.db

# 重新初始化
cd backend
python init_db.py
```

---

## 📊 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    真机 (Android)                    │
│  ┌──────────────────────────────────────────────┐  │
│  │         ImageGen APP (Flutter)               │  │
│  │  - 用户注册/登录                             │  │
│  │  - 图像生成                                  │  │
│  │  - 历史记录                                  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓ HTTP
                 192.168.18.2:8001
                        ↓
┌─────────────────────────────────────────────────────┐
│              本地电脑 (Windows)                      │
│  ┌──────────────────────────────────────────────┐  │
│  │      FastAPI 后端服务 (Python)               │  │
│  │  - 用户认证                                  │  │
│  │  - 图像生成任务                              │  │
│  │  - 数据管理                                  │  │
│  └──────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌──────────────────────────────────────────────┐  │
│  │      SQLite 数据库                           │  │
│  │  - 用户数据                                  │  │
│  │  - 生成任务                                  │  │
│  │  - 结果数据                                  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 📝 总结

**本地电脑需要做的事情：**

1. ✅ 激活虚拟环境
2. ✅ 启动后端服务（8001 端口）
3. ✅ 确保防火墙允许 8001 端口

**然后 APP 就可以连接到后端进行注册了！**

---

**现在可以开始测试应用了！** 🚀

