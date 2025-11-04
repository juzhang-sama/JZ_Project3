# 📱 真机安装和测试指南

## 🔧 问题分析

**错误原因：**
```
DioException [connection error]: Connection failed
address = localhost, port = 8000
```

**根本原因：**
- 应用在真机上尝试连接到 `localhost:8000`
- `localhost` 在真机上指的是手机本身，而不是电脑
- 真机无法访问电脑上的 `localhost`

---

## ✅ 解决方案

### 1️⃣ **配置更新**

已将 API 连接地址从 `localhost` 改为电脑 IP 地址：

**修改的文件：**
- `frontend/lib/services/auth_service.dart`
  - 从: `http://localhost:8000/api/v1/auth`
  - 改为: `http://192.168.18.2:8000/api/v1/auth`

- `frontend/lib/services/api_service.dart`
  - 从: `http://localhost:8000/api/v1`
  - 改为: `http://192.168.18.2:8000/api/v1`

**你的电脑 IP 地址：** `192.168.18.2`

### 2️⃣ **新 APK 已生成**

- **文件名：** `app-release.apk`
- **位置：** `D:\JZ_Project3\app-release.apk`
- **大小：** 21.54 MB
- **配置：** 使用新的 IP 地址 `192.168.18.2:8000`

---

## 📲 安装到真机

### 前置条件

1. **手机和电脑在同一个 WiFi 网络上**
   - 确保手机连接到 `192.168.18.x` 网段的 WiFi

2. **启用 USB 调试**
   - 设置 → 开发者选项 → USB 调试（打开）

3. **连接 USB 线**
   - 用 USB 线连接手机和电脑

4. **安装 ADB**
   - ADB 已随 Android SDK 安装

### 安装步骤

#### 方式 1：使用 ADB 命令（推荐）

```powershell
# 进入项目根目录
cd D:\JZ_Project3

# 检查设备连接
adb devices

# 安装 APK
adb install -r app-release.apk

# 启动应用
adb shell am start -n com.example.frontend/.MainActivity
```

#### 方式 2：直接复制到手机

1. 将 `app-release.apk` 复制到手机存储
2. 使用文件管理器打开 APK 文件
3. 点击"安装"

---

## 🧪 测试步骤

### 1️⃣ **启动后端服务**

```powershell
cd D:\JZ_Project3\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**验证后端运行：**
```powershell
# 在浏览器中打开
http://192.168.18.2:8000/docs
```

### 2️⃣ **打开应用**

1. 在手机上找到 "ImageGen" 应用
2. 点击打开

### 3️⃣ **注册新用户**

1. 点击"注册"
2. 填写信息：
   - 用户名：`test`
   - 邮箱：`test@example.com`
   - 密码：`password123`
   - 确认密码：`password123`
3. 点击"注册"按钮

### 4️⃣ **验证连接**

如果注册成功，说明：
- ✅ 手机已成功连接到电脑
- ✅ 后端 API 正常工作
- ✅ 网络连接正常

---

## 🔍 故障排除

### 问题 1：仍然显示 `localhost` 错误

**原因：** 旧 APK 仍在手机上

**解决方案：**
```powershell
# 卸载旧应用
adb uninstall com.example.frontend

# 重新安装新 APK
adb install -r app-release.apk
```

### 问题 2：无法连接到 `192.168.18.2:8000`

**检查清单：**
1. ✅ 手机和电脑在同一 WiFi 网络
2. ✅ 后端服务正在运行
3. ✅ 防火墙允许 8000 端口
4. ✅ IP 地址正确（`192.168.18.2`）

**测试连接：**
```powershell
# 在手机浏览器中打开
http://192.168.18.2:8000/docs
```

### 问题 3：防火墙阻止连接

**Windows 防火墙设置：**
1. 打开 Windows Defender 防火墙
2. 点击"允许应用通过防火墙"
3. 找到 Python 或 FastAPI
4. 确保已勾选"专用"和"公用"

---

## 📝 配置说明

### IP 地址说明

- **192.168.18.2** - 你的电脑 IP 地址（以太网）
- **192.168.18.x** - 手机应该在这个网段

### 如果 IP 地址不同

如果你的电脑 IP 地址不是 `192.168.18.2`，需要：

1. 查看你的电脑 IP：
   ```powershell
   ipconfig
   ```

2. 修改 Flutter 配置文件：
   - `frontend/lib/services/auth_service.dart`
   - `frontend/lib/services/api_service.dart`

3. 将 `192.168.18.2` 替换为你的实际 IP 地址

4. 重新构建 APK：
   ```powershell
   cd frontend
   flutter build apk --release
   ```

---

## ✅ 成功标志

当你看到以下情况时，说明配置成功：

1. ✅ 应用成功连接到后端
2. ✅ 注册/登录功能正常
3. ✅ 没有 `localhost` 连接错误
4. ✅ 可以查看用户信息

---

## 🚀 下一步

1. 测试所有功能
2. 验证图像生成功能
3. 检查历史记录
4. 测试用户资料管理

祝你使用愉快！🎉

