# 🚀 完整的本地运行指南

## 📱 APP 在真机上注册失败的原因和解决方案

### 问题分析
你的 APP 在真机上注册时出现连接错误，原因是：

1. **后端服务没有运行** - 本地电脑上没有启动 FastAPI 服务
2. **数据库配置错误** - 配置使用 PostgreSQL，但电脑上没有安装
3. **端口冲突** - 8000 端口被占用

### 解决方案已实施
✅ 修改数据库配置为 SQLite（无需额外安装）
✅ 启动后端服务在 8001 端口
✅ 更新 APP 配置使用新的端口
✅ 生成新的 APK 文件

---

## 🖥️ 本地电脑需要进行的操作

### 必须做的事情

#### 1️⃣ 启动后端服务

**最简单的方式：**
```powershell
cd D:\JZ_Project3\backend
.\start_backend_simple.ps1
```

**或者手动启动：**
```powershell
cd D:\JZ_Project3\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

**成功的标志：**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

#### 2️⃣ 验证后端是否运行

在浏览器中访问：
```
http://localhost:8001
```

应该看到 JSON 响应。

#### 3️⃣ 确保防火墙允许 8001 端口

- 打开 Windows Defender 防火墙
- 点击"允许应用通过防火墙"
- 确保 Python 在允许列表中

---

## 📲 真机上的操作

### 1. 安装新 APK

```powershell
cd D:\JZ_Project3
adb install -r app-release-port8001.apk
```

### 2. 打开应用

- 在手机上打开 ImageGen 应用
- 点击"注册"按钮

### 3. 填写注册信息

- 用户名：任意（例如：testuser）
- 邮箱：任意有效邮箱（例如：test@example.com）
- 密码：至少 8 个字符（例如：password123）

### 4. 点击注册

- 应该成功注册
- 自动登录
- 进入主界面

---

## 📊 系统配置信息

### 后端服务
- **地址：** `http://0.0.0.0:8001`
- **API 基础 URL：** `http://192.168.18.2:8001/api/v1`
- **数据库：** SQLite (`backend/image_gen.db`)
- **API 文档：** `http://localhost:8001/docs`

### APP 配置
- **包名：** `com.example.frontend`
- **API 端点：** `http://192.168.18.2:8001/api/v1`
- **认证端点：** `http://192.168.18.2:8001/api/v1/auth`
- **APK 文件：** `app-release-port8001.apk`

### 网络要求
- ✅ 手机和电脑在同一 WiFi 网络
- ✅ 电脑 IP 地址：`192.168.18.2`
- ✅ 后端服务运行在 `0.0.0.0:8001`
- ✅ 防火墙允许 8001 端口

---

## 🔄 完整的启动流程

### 第一次启动

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

### 后续启动

```powershell
# 1. 进入后端目录
cd D:\JZ_Project3\backend

# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 3. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

## ✅ 检查清单

在安装 APP 之前，请确保：

- [ ] 后端服务已启动
- [ ] 可以访问 `http://localhost:8001`
- [ ] 手机和电脑在同一 WiFi
- [ ] 防火墙允许 8001 端口
- [ ] 新 APK 已安装

---

## 🐛 常见问题

### Q1: 后端启动失败，显示"端口被占用"

**A:** 使用以下命令杀死占用端口的进程：
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Q2: APP 仍然无法连接

**A:** 检查以下几点：
1. 后端服务是否运行？
2. 手机和电脑是否在同一 WiFi？
3. 防火墙是否允许 8001 端口？
4. 电脑 IP 是否是 192.168.18.2？

### Q3: 数据库错误

**A:** 重新初始化数据库：
```powershell
cd D:\JZ_Project3\backend
rm image_gen.db
python init_db.py
```

---

## 📚 相关文档

- `BACKEND_SETUP_COMPLETE.md` - 后端配置详细指南
- `LOCAL_SETUP_GUIDE.md` - 本地设置指南
- `QUICK_FIX_SUMMARY.md` - 快速参考
- `REAL_DEVICE_INSTALLATION_GUIDE.md` - 真机安装指南

---

## 🎯 下一步

1. ✅ 启动后端服务
2. ✅ 安装新 APK
3. ✅ 在真机上测试注册
4. ✅ 测试其他功能

---

**现在可以开始测试应用了！** 🚀

如有问题，请参考相关文档或检查故障排除部分。

