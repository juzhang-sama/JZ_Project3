# 🔄 配置对比：修改前后

## 📊 API 端点配置对比

### 文件 1：`frontend/lib/services/auth_service.dart`

#### ❌ 修改前（导致错误）
```dart
class AuthService {
  static const String baseUrl = 'http://localhost:8000/api/v1/auth';
  late Dio _dio;
  final _storage = const FlutterSecureStorage();

  AuthService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,  // ❌ 使用 localhost
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
  }
  // ...
}
```

**问题：**
- 在真机上，`localhost` 指的是手机本身
- 真机无法访问电脑上的 `localhost:8000`
- 导致连接错误

#### ✅ 修改后（已修复）
```dart
class AuthService {
  static const String baseUrl = 'http://192.168.18.2:8000/api/v1/auth';
  late Dio _dio;
  final _storage = const FlutterSecureStorage();

  AuthService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,  // ✅ 使用电脑 IP 地址
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
  }
  // ...
}
```

**优点：**
- 真机可以访问电脑上的服务
- 需要手机和电脑在同一网络
- 支持真实设备测试

---

### 文件 2：`frontend/lib/services/api_service.dart`

#### ❌ 修改前
```dart
class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  late Dio _dio;

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,  // ❌ 使用 localhost
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
  }
  // ...
}
```

#### ✅ 修改后
```dart
class ApiService {
  static const String baseUrl = 'http://192.168.18.2:8000/api/v1';
  late Dio _dio;

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,  // ✅ 使用电脑 IP 地址
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
  }
  // ...
}
```

---

## 🌐 网络连接对比

### 场景 1：Android 模拟器（旧配置）
```
模拟器 → localhost:8000 → 电脑上的后端
✅ 工作正常（模拟器有特殊的 localhost 映射）
```

### 场景 2：真实设备（旧配置）
```
真机 → localhost:8000 → 手机本身（❌ 错误！）
❌ 连接失败
```

### 场景 3：真实设备（新配置）
```
真机 → 192.168.18.2:8000 → 电脑上的后端
✅ 工作正常（需要同一网络）
```

---

## 📋 配置对比表

| 方面 | 旧配置 | 新配置 |
|------|--------|--------|
| **API 基础 URL** | `http://localhost:8000/api/v1` | `http://192.168.18.2:8000/api/v1` |
| **认证 URL** | `http://localhost:8000/api/v1/auth` | `http://192.168.18.2:8000/api/v1/auth` |
| **模拟器支持** | ✅ 支持 | ✅ 支持 |
| **真机支持** | ❌ 不支持 | ✅ 支持 |
| **网络要求** | 无 | 同一 WiFi 网络 |
| **防火墙要求** | 无 | 允许 8000 端口 |

---

## 🔧 使用场景

### 使用旧配置（localhost）
- ✅ Android 模拟器
- ✅ iOS 模拟器
- ❌ 真实 Android 设备
- ❌ 真实 iOS 设备

### 使用新配置（IP 地址）
- ✅ Android 模拟器（需要特殊配置）
- ✅ iOS 模拟器（需要特殊配置）
- ✅ 真实 Android 设备
- ✅ 真实 iOS 设备

---

## 🚀 迁移步骤

1. **更新配置文件**
   - ✅ 已完成

2. **重新构建 APK**
   - ✅ 已完成

3. **安装新 APK**
   - 使用 `adb install -r app-release.apk`

4. **测试连接**
   - 打开应用并尝试注册

---

## 💡 技术说明

### 为什么 localhost 在真机上不工作？

**localhost 的含义：**
- 在电脑上：指的是电脑本身（127.0.0.1）
- 在真机上：指的是手机本身（127.0.0.1）

**解决方案：**
- 使用电脑的实际 IP 地址（192.168.18.2）
- 真机可以通过网络访问电脑

### 为什么模拟器可以使用 localhost？

**Android 模拟器的特殊处理：**
- Android 模拟器有特殊的 localhost 映射
- `10.0.2.2` 在模拟器中指的是主机的 localhost
- 这是 Android 模拟器的内置功能

---

## ✅ 验证清单

- [x] 修改 `auth_service.dart`
- [x] 修改 `api_service.dart`
- [x] 重新构建 APK
- [x] 生成新 APK 文件
- [x] 提交到 Git
- [x] 创建文档

**现在可以在真机上测试了！** 🎉

