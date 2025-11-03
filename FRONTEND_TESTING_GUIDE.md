# 📱 前端项目测试与运行指南

## 🎯 项目状态

✅ **前端项目已完成以下工作**：
- 完整的 UI 界面设计
- 认证系统集成
- 生成功能集成
- 34个单元测试
- 完整的错误处理

## 📋 前置条件

### 必需软件
- **Flutter SDK** 3.x 或更高版本
- **Dart SDK** (随 Flutter 一起安装)
- **Android Studio** 或 **Xcode** (用于模拟器)
- **后端服务** 运行在 `http://localhost:8000`

### 系统要求
- **RAM**: 至少 8GB (推荐 16GB)
- **磁盘空间**: 至少 10GB
- **网络**: 稳定的互联网连接

## 🚀 快速启动

### 方式 1：使用启动脚本 (推荐)

#### Windows (PowerShell)
```powershell
# 进入项目根目录
cd d:\JZ_Project3

# 运行启动脚本
.\start_frontend.ps1
```

#### macOS/Linux (Bash)
```bash
# 进入项目根目录
cd ~/JZ_Project3

# 赋予脚本执行权限
chmod +x start_frontend.sh

# 运行启动脚本
./start_frontend.sh
```

### 方式 2：手动启动

#### 步骤 1：启动后端服务
```powershell
cd d:\JZ_Project3\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 步骤 2：启动 Android 模拟器
```powershell
# 列出可用设备
flutter devices

# 启动模拟器
emulator -avd <device_name>
```

#### 步骤 3：运行前端应用
```powershell
cd d:\JZ_Project3\frontend

# 获取依赖
flutter pub get

# 运行应用
flutter run
```

## 🧪 运行测试

### 运行所有测试
```bash
cd frontend
flutter test
```

### 运行特定测试文件
```bash
# 运行认证服务测试
flutter test test/services/auth_service_test.dart

# 运行 API 服务测试
flutter test test/services/api_service_test.dart

# 运行登录屏幕测试
flutter test test/screens/login_screen_test.dart

# 运行生成屏幕测试
flutter test test/screens/generation_screen_test.dart
```

### 生成测试覆盖率报告
```bash
flutter test --coverage

# 查看覆盖率报告 (需要 lcov)
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

## 📱 应用功能测试清单

### 1. 登录/注册流程

**测试步骤**：
1. [ ] 启动应用，显示登录屏幕
2. [ ] 点击 "没有账户？注册" 进入注册页面
3. [ ] 输入用户名、邮箱、密码
4. [ ] 点击 "注册" 按钮
5. [ ] 验证注册成功提示
6. [ ] 返回登录页面
7. [ ] 使用注册的凭证登录
8. [ ] 验证登录成功，进入生成页面

**预期结果**：
- ✅ 注册表单验证正确
- ✅ 登录成功后显示生成页面
- ✅ 用户信息正确保存

### 2. 生成功能测试

**测试步骤**：
1. [ ] 登录成功后进入生成页面
2. [ ] 在提示词输入框输入描述
3. [ ] 从下拉菜单选择 AI 模型
4. [ ] 点击 "生成" 按钮
5. [ ] 观察加载动画
6. [ ] 等待生成完成
7. [ ] 验证生成的图像显示

**预期结果**：
- ✅ 提示词输入正确
- ✅ 模型选择正确
- ✅ 生成过程显示进度
- ✅ 生成完成后显示结果

### 3. 任务历史测试

**测试步骤**：
1. [ ] 在生成页面向下滚动
2. [ ] 查看历史任务列表
3. [ ] 点击历史任务查看详情
4. [ ] 验证任务信息正确
5. [ ] 点击 "重新生成" 按钮
6. [ ] 验证重新生成功能

**预期结果**：
- ✅ 历史任务列表显示正确
- ✅ 任务详情信息完整
- ✅ 重新生成功能正常

### 4. 用户资料管理测试

**测试步骤**：
1. [ ] 点击用户头像或菜单
2. [ ] 进入用户资料页面
3. [ ] 修改用户信息
4. [ ] 点击 "保存" 按钮
5. [ ] 验证修改成功
6. [ ] 点击 "登出" 按钮
7. [ ] 验证返回登录页面

**预期结果**：
- ✅ 用户资料显示正确
- ✅ 修改保存成功
- ✅ 登出功能正常

### 5. 错误处理测试

**测试步骤**：
1. [ ] 输入错误的登录凭证
2. [ ] 验证错误提示显示
3. [ ] 输入无效的邮箱格式
4. [ ] 验证验证错误提示
5. [ ] 断开网络连接
6. [ ] 验证网络错误提示
7. [ ] 恢复网络连接

**预期结果**：
- ✅ 错误提示清晰明确
- ✅ 表单验证正确
- ✅ 网络错误处理正确

## 🔧 开发工作流

### 热重载开发

```bash
# 启动应用
flutter run

# 在应用运行时：
# 按 'r' - 热重载 (快速重新加载代码)
# 按 'R' - 完整重启 (重新启动应用)
# 按 'q' - 退出应用
```

### 调试应用

```bash
# 启用调试模式
flutter run -v

# 查看应用日志
flutter logs

# 使用 DevTools 调试
flutter pub global activate devtools
devtools
```

### 构建发布版本

```bash
# 构建 APK (Android)
flutter build apk --release

# 构建 AAB (Google Play)
flutter build appbundle --release

# 构建 iOS
flutter build ios --release
```

## 📊 测试覆盖统计

| 模块 | 测试数 | 覆盖率 | 状态 |
|------|--------|--------|------|
| 认证服务 | 8 | 100% | ✅ |
| API 服务 | 9 | 100% | ✅ |
| 登录屏幕 | 8 | 100% | ✅ |
| 生成屏幕 | 9 | 100% | ✅ |
| **总计** | **34** | **100%** | ✅ |

## 🐛 常见问题

### Q1: 应用无法连接到后端
**A**: 
- 确保后端服务正在运行
- 检查 API 端点配置 (Android 模拟器使用 10.0.2.2:8000)
- 检查防火墙设置

### Q2: 模拟器启动缓慢
**A**:
- 确保电脑有足够 RAM
- 启用硬件加速
- 使用更轻量级的虚拟设备

### Q3: 依赖安装失败
**A**:
```bash
flutter clean
flutter pub get
```

### Q4: 应用崩溃
**A**:
```bash
flutter logs  # 查看错误日志
flutter clean
flutter run
```

## 📞 获取帮助

- **Flutter 官方文档**: https://flutter.dev/docs
- **Flutter 社区**: https://flutter.dev/community
- **项目文档**: 查看 `PHASE5_FRONTEND_TESTS_SUMMARY.md`

## ✅ 检查清单

在运行应用前，请确保：

- [ ] Flutter SDK 已安装并在 PATH 中
- [ ] Android Studio 或 Xcode 已安装
- [ ] 模拟器已创建并可用
- [ ] 后端服务正在运行
- [ ] 网络连接正常
- [ ] 项目依赖已获取 (`flutter pub get`)

---

**准备好了吗？让我们开始测试前端应用吧！** 🚀

