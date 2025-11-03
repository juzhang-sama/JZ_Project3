# 🚀 前端项目本地运行指南

## 📋 前置要求

### 1. Flutter SDK 安装

#### Windows 安装步骤

1. **下载 Flutter SDK**
   - 访问 https://flutter.dev/docs/get-started/install/windows
   - 下载最新的 Flutter SDK (3.x 或更高版本)

2. **解压 Flutter SDK**
   ```powershell
   # 推荐解压到 C:\flutter 或 D:\flutter
   # 例如：D:\flutter
   ```

3. **添加 Flutter 到 PATH**
   - 打开系统环境变量设置
   - 添加 `D:\flutter\bin` 到 PATH
   - 重启 PowerShell 或 CMD

4. **验证安装**
   ```powershell
   flutter --version
   flutter doctor
   ```

### 2. Android 模拟器设置

#### 选项 A：使用 Android Studio 模拟器

1. **安装 Android Studio**
   - 下载：https://developer.android.com/studio

2. **创建虚拟设备**
   - 打开 Android Studio
   - Tools → Device Manager
   - 创建新的虚拟设备 (推荐 Pixel 4 或更高)
   - 选择 API 级别 30 或更高

3. **启动模拟器**
   ```powershell
   # 列出可用设备
   flutter devices
   
   # 启动特定模拟器
   emulator -avd <device_name>
   ```

#### 选项 B：使用 iOS 模拟器 (仅 macOS)

```bash
open -a Simulator
```

### 3. 后端服务运行

确保后端 FastAPI 服务正在运行：

```powershell
cd d:\JZ_Project3\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🛠️ 前端项目设置

### 1. 获取依赖

```powershell
cd d:\JZ_Project3\frontend

# 获取所有依赖
flutter pub get

# 或者使用 pub upgrade 获取最新版本
flutter pub upgrade
```

### 2. 配置 API 端点

编辑 `frontend/lib/services/api_service.dart`，确保 API 端点正确：

```dart
class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1';
  // 注意：在 Android 模拟器中，10.0.2.2 代表主机的 localhost
  // 在 iOS 模拟器中，使用 localhost:8000
  // 在真实设备上，使用实际的服务器 IP 地址
}
```

### 3. 运行项目

#### 在 Android 模拟器上运行

```powershell
cd d:\JZ_Project3\frontend

# 列出可用设备
flutter devices

# 运行应用
flutter run

# 或指定设备
flutter run -d <device_id>
```

#### 在 iOS 模拟器上运行 (macOS)

```bash
cd frontend
flutter run -d "iPhone 14"
```

#### 在真实设备上运行

```powershell
# 启用 USB 调试
# 连接设备到电脑

flutter devices  # 确认设备已连接

flutter run
```

## 📱 应用功能测试

### 1. 登录/注册流程

1. 启动应用后，会看到登录屏幕
2. 点击 "没有账户？注册" 进入注册页面
3. 输入用户名、邮箱、密码进行注册
4. 注册成功后返回登录页面
5. 使用注册的凭证登录

### 2. 生成功能测试

1. 登录成功后进入生成页面
2. 在提示词输入框输入描述 (例如："一只可爱的猫咪")
3. 从下拉菜单选择 AI 模型
4. 点击 "生成" 按钮
5. 等待生成完成，查看结果

### 3. 任务历史

1. 在生成页面向下滚动查看历史任务
2. 点击历史任务可查看详情
3. 可以重新生成相同的提示词

## 🐛 常见问题

### 问题 1：无法连接到后端服务

**症状**：应用启动后无法登录，显示连接错误

**解决方案**：
1. 确保后端服务正在运行
2. 检查 API 端点配置是否正确
3. 在 Android 模拟器中，使用 `10.0.2.2:8000` 而不是 `localhost:8000`
4. 检查防火墙设置

### 问题 2：模拟器启动缓慢

**症状**：模拟器启动需要很长时间

**解决方案**：
1. 确保电脑有足够的 RAM (至少 8GB)
2. 启用硬件加速
3. 使用更轻量级的虚拟设备配置

### 问题 3：依赖安装失败

**症状**：`flutter pub get` 失败

**解决方案**：
```powershell
# 清除缓存
flutter clean

# 重新获取依赖
flutter pub get

# 或使用 pub upgrade
flutter pub upgrade
```

### 问题 4：应用崩溃

**症状**：应用启动后立即崩溃

**解决方案**：
1. 查看日志：`flutter logs`
2. 检查后端服务是否正在运行
3. 清除应用数据：`flutter clean`
4. 重新运行：`flutter run`

## 📊 项目结构

```
frontend/
├── lib/
│   ├── main.dart                 # 应用入口
│   ├── screens/
│   │   ├── login_screen.dart     # 登录屏幕
│   │   ├── register_screen.dart  # 注册屏幕
│   │   └── generation_screen.dart # 生成屏幕
│   ├── services/
│   │   ├── api_service.dart      # API 服务
│   │   └── auth_service.dart     # 认证服务
│   ├── providers/
│   │   └── auth_provider.dart    # 认证状态管理
│   └── models/
│       └── user.dart             # 用户模型
├── test/
│   ├── services/                 # 服务测试
│   └── screens/                  # 屏幕测试
└── pubspec.yaml                  # 项目配置
```

## 🎯 开发工作流

### 1. 热重载开发

```powershell
# 启动应用
flutter run

# 在应用运行时，按 'r' 进行热重载
# 按 'R' 进行完整重启
# 按 'q' 退出
```

### 2. 运行测试

```powershell
# 运行所有测试
flutter test

# 运行特定测试文件
flutter test test/services/auth_service_test.dart

# 生成覆盖率报告
flutter test --coverage
```

### 3. 构建发布版本

```powershell
# 构建 APK (Android)
flutter build apk --release

# 构建 AAB (Google Play)
flutter build appbundle --release

# 构建 iOS
flutter build ios --release
```

## 📞 支持

如有问题，请参考：
- Flutter 官方文档：https://flutter.dev/docs
- Flutter 社区：https://flutter.dev/community
- 项目文档：查看 `PHASE5_FRONTEND_TESTS_SUMMARY.md`

---

**准备好了吗？让我们开始运行前端应用吧！** 🚀

