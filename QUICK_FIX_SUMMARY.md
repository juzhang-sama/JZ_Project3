# 🔧 快速修复总结

## 问题
真机注册时报错：
```
DioException [connection error]: Connection failed
address = localhost, port = 8000
```

## 原因
应用尝试连接到 `localhost:8000`，但真机上 `localhost` 指的是手机本身，不是电脑。

## 解决方案

### ✅ 已完成的修改

1. **修改 API 配置**
   - `frontend/lib/services/auth_service.dart`
   - `frontend/lib/services/api_service.dart`
   - 将 `localhost` 改为 `192.168.18.2`（你的电脑 IP）

2. **重新构建 APK**
   - 新 APK 已生成：`D:\JZ_Project3\app-release.apk`
   - 大小：21.54 MB
   - 配置：使用新的 IP 地址

### 📲 安装新 APK

```powershell
# 进入项目目录
cd D:\JZ_Project3

# 检查设备
adb devices

# 卸载旧应用（如果存在）
adb uninstall com.example.frontend

# 安装新 APK
adb install -r app-release.apk
```

### 🧪 测试

1. **启动后端**
   ```powershell
   cd backend
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **打开应用并注册**
   - 应该能成功连接到后端
   - 注册应该成功

### ⚠️ 重要提醒

- ✅ 手机和电脑必须在同一 WiFi 网络
- ✅ 后端服务必须运行
- ✅ 防火墙必须允许 8000 端口

### 🔍 如果还有问题

1. 检查 IP 地址是否正确
   ```powershell
   ipconfig
   ```

2. 验证后端是否运行
   ```powershell
   # 在浏览器打开
   http://192.168.18.2:8000/docs
   ```

3. 如果 IP 不同，需要修改配置并重新构建 APK

---

**现在可以安装新 APK 并测试了！** 🚀

