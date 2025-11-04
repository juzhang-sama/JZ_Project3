# 🖥️ 本地电脑运行配置指南

## ⚠️ 问题分析

你的 APP 在真机上注册时出现连接错误，这是因为：

1. **APP 配置了 IP 地址：** `192.168.18.2:8000`
2. **但后端服务没有运行** 或 **配置不正确**
3. **数据库连接失败** 或 **数据库不存在**

---

## 🔧 本地电脑需要进行的操作

### 第 1 步：检查 Python 环境

```powershell
# 检查 Python 版本
python --version

# 应该是 Python 3.8 或更高版本
```

### 第 2 步：进入后端目录并激活虚拟环境

```powershell
cd D:\JZ_Project3\backend

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 如果出现权限错误，运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 第 3 步：安装依赖

```powershell
# 确保在虚拟环境中
pip install -r requirements.txt

# 如果需要升级 pip
python -m pip install --upgrade pip
```

### 第 4 步：初始化数据库

```powershell
# 运行数据库初始化脚本
python init_db.py

# 这会创建 SQLite 数据库文件
```

### 第 5 步：启动后端服务

```powershell
# 方式 1：使用 uvicorn 直接运行（推荐）
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式 2：使用 Python 直接运行
python app/main.py
```

---

## 📋 完整的启动步骤

### 一键启动脚本

创建文件 `start_backend.ps1`：

```powershell
# 进入后端目录
cd D:\JZ_Project3\backend

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖（如果需要）
pip install -r requirements.txt

# 初始化数据库（如果需要）
python init_db.py

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

然后运行：
```powershell
.\start_backend.ps1
```

---

## 🔍 验证后端是否正常运行

### 1. 检查服务是否启动

在浏览器中访问：
```
http://localhost:8000
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

### 2. 检查健康状态

访问：
```
http://localhost:8000/health
```

应该看到：
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### 3. 查看 API 文档

访问：
```
http://localhost:8000/docs
```

这会打开 Swagger UI，可以看到所有 API 端点

---

## 🗄️ 数据库配置

### 当前配置

后端使用 **SQLite** 数据库（开发环境）：

```python
# 在 backend/app/config.py 中
DATABASE_URL: str = "postgresql://image_gen:password@localhost:5432/image_gen_dev"
```

但实际上应该使用 SQLite：

```python
DATABASE_URL: str = "sqlite:///./image_gen.db"
```

### 初始化数据库

```powershell
cd D:\JZ_Project3\backend
python init_db.py
```

这会创建 `image_gen.db` 文件

---

## 🚀 完整的启动流程

### 第一次启动

```powershell
# 1. 进入后端目录
cd D:\JZ_Project3\backend

# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库
python init_db.py

# 5. 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 后续启动

```powershell
# 1. 进入后端目录
cd D:\JZ_Project3\backend

# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 3. 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ 启动成功的标志

当你看到以下输出时，说明后端已成功启动：

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## 🔗 APP 连接配置

APP 已配置为连接到：
- **IP 地址：** `192.168.18.2`
- **端口：** `8000`
- **API 基础 URL：** `http://192.168.18.2:8000/api/v1`

确保：
1. ✅ 手机和电脑在同一 WiFi 网络
2. ✅ 电脑 IP 地址是 `192.168.18.2`
3. ✅ 后端服务运行在 `0.0.0.0:8000`
4. ✅ 防火墙允许 8000 端口

---

## 🐛 故障排除

### 问题 1：无法连接到 192.168.18.2:8000

**解决方案：**
```powershell
# 检查电脑 IP 地址
ipconfig

# 查找 IPv4 地址，应该是 192.168.18.x
```

### 问题 2：后端启动失败

**解决方案：**
```powershell
# 检查依赖是否安装
pip list

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 问题 3：数据库错误

**解决方案：**
```powershell
# 删除旧数据库
rm image_gen.db

# 重新初始化
python init_db.py
```

### 问题 4：端口被占用

**解决方案：**
```powershell
# 查找占用 8000 端口的进程
netstat -ano | findstr :8000

# 杀死进程（替换 PID）
taskkill /PID <PID> /F

# 或使用不同的端口
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

---

## 📝 总结

**本地电脑需要做的事情：**

1. ✅ 激活虚拟环境
2. ✅ 安装 Python 依赖
3. ✅ 初始化数据库
4. ✅ 启动 FastAPI 后端服务
5. ✅ 确保防火墙允许 8000 端口

**然后 APP 就可以连接到后端进行注册了！**

