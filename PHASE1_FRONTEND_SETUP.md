# 第一阶段：前端项目初始化

## 📋 任务概述

**目标**：创建Flutter项目结构，配置所有依赖，创建基础框架
**时间**：第1-2天（15小时）
**完成标志**：前端项目可编译运行，基础框架就绪

---

## 🚀 第一步：创建Flutter项目

### 1.1 创建项目
```bash
# 创建Flutter项目
flutter create image_gen_app

# 进入项目目录
cd image_gen_app

# 验证Flutter环境
flutter doctor
```

### 1.2 项目结构
```
image_gen_app/
├── lib/
│   ├── main.dart                    # 应用入口
│   ├── config/
│   │   ├── api_config.dart          # API配置
│   │   └── app_theme.dart           # 主题配置
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── register_screen.dart
│   │   ├── home/
│   │   │   └── home_screen.dart
│   │   ├── generate/
│   │   │   ├── prompt_input_screen.dart
│   │   │   ├── model_selection_screen.dart
│   │   │   └── generation_progress_screen.dart
│   │   ├── result/
│   │   │   ├── result_display_screen.dart
│   │   │   └── history_screen.dart
│   │   └── profile/
│   │       └── profile_screen.dart
│   ├── providers/
│   │   ├── auth_provider.dart
│   │   ├── generation_provider.dart
│   │   └── user_provider.dart
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── storage_service.dart
│   │   └── image_service.dart
│   ├── models/
│   │   ├── user.dart
│   │   ├── generation_task.dart
│   │   ├── model.dart
│   │   └── result.dart
│   ├── widgets/
│   │   ├── common/
│   │   │   ├── loading_widget.dart
│   │   │   └── error_widget.dart
│   │   └── custom/
│   │       ├── prompt_input_field.dart
│   │       └── model_selector.dart
│   └── utils/
│       ├── constants.dart
│       └── validators.dart
├── test/
├── pubspec.yaml
└── README.md
```

---

## 📦 第二步：配置依赖

### 2.1 编辑pubspec.yaml
```yaml
name: image_gen_app
description: A simple AI image generation app.
publish_to: 'none'

version: 0.1.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # HTTP和API
  dio: ^5.3.0
  http: ^1.1.0

  # 状态管理
  provider: ^6.0.0
  riverpod: ^2.4.0
  flutter_riverpod: ^2.4.0

  # 路由
  go_router: ^11.0.0

  # 本地存储
  hive: ^2.2.0
  hive_flutter: ^1.1.0
  shared_preferences: ^2.2.0

  # 图片处理
  cached_network_image: ^3.3.0
  image_picker: ^1.0.0
  image_gallery_saver: ^2.0.0

  # 分享
  share_plus: ^7.0.0

  # 国际化
  intl: ^0.19.0

  # 日期时间
  timeago: ^3.5.0

  # JSON序列化
  json_serializable: ^6.7.0
  json_annotation: ^4.8.0

  # 日志
  logger: ^2.0.0

  # 工具
  get_it: ^7.6.0
  freezed_annotation: ^2.4.0

dev_dependencies:
  flutter_test:
    sdk: flutter

  flutter_lints: ^2.0.0
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
  freezed: ^2.4.0

flutter:
  uses-material-design: true

  # 资源
  assets:
    - assets/images/
    - assets/icons/

  # 字体
  fonts:
    - family: Roboto
      fonts:
        - asset: assets/fonts/Roboto-Regular.ttf
        - asset: assets/fonts/Roboto-Bold.ttf
          weight: 700
```

### 2.2 获取依赖
```bash
flutter pub get
```

---

## 🔧 第三步：配置文件

### 3.1 创建lib/config/api_config.dart
```dart
class ApiConfig {
  // API基础URL
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  // 超时时间（毫秒）
  static const int connectTimeout = 30000;
  static const int receiveTimeout = 30000;
  
  // 端点
  static const String authLogin = '/auth/login';
  static const String authRegister = '/auth/register';
  static const String authRefresh = '/auth/refresh';
  static const String authLogout = '/auth/logout';
  
  static const String usersMe = '/users/me';
  static const String usersAvatar = '/users/me/avatar';
  
  static const String generationGenerate = '/generation/generate';
  static const String generationTasks = '/generation/tasks';
  static const String generationHistory = '/generation/history';
  
  static const String models = '/models';
  
  static const String results = '/results';
}
```

### 3.2 创建lib/config/app_theme.dart
```dart
import 'package:flutter/material.dart';

class AppTheme {
  // 颜色
  static const Color primaryColor = Color(0xFF6200EE);
  static const Color secondaryColor = Color(0xFF03DAC6);
  static const Color backgroundColor = Color(0xFFFAFAFA);
  static const Color errorColor = Color(0xFFB00020);
  
  // 主题
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: primaryColor,
      brightness: Brightness.light,
    ),
    appBarTheme: const AppBarTheme(
      elevation: 0,
      centerTitle: true,
    ),
  );
  
  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: primaryColor,
      brightness: Brightness.dark,
    ),
  );
}
```

---

## 📝 第四步：创建基础模型

### 4.1 创建lib/models/user.dart
```dart
class User {
  final int id;
  final String username;
  final String email;
  final String? avatarUrl;
  final DateTime createdAt;
  
  User({
    required this.id,
    required this.username,
    required this.email,
    this.avatarUrl,
    required this.createdAt,
  });
  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      avatarUrl: json['avatar_url'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'avatar_url': avatarUrl,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
```

### 4.2 创建lib/models/generation_task.dart
```dart
class GenerationTask {
  final int id;
  final String prompt;
  final String modelName;
  final String status; // pending, processing, completed, failed
  final DateTime createdAt;
  final DateTime? completedAt;
  final String? errorMessage;
  
  GenerationTask({
    required this.id,
    required this.prompt,
    required this.modelName,
    required this.status,
    required this.createdAt,
    this.completedAt,
    this.errorMessage,
  });
  
  factory GenerationTask.fromJson(Map<String, dynamic> json) {
    return GenerationTask(
      id: json['id'],
      prompt: json['prompt'],
      modelName: json['model_name'],
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
      completedAt: json['completed_at'] != null 
        ? DateTime.parse(json['completed_at']) 
        : null,
      errorMessage: json['error_message'],
    );
  }
}
```

### 4.3 创建lib/models/result.dart
```dart
class Result {
  final int id;
  final int taskId;
  final String imageUrl;
  final DateTime createdAt;
  
  Result({
    required this.id,
    required this.taskId,
    required this.imageUrl,
    required this.createdAt,
  });
  
  factory Result.fromJson(Map<String, dynamic> json) {
    return Result(
      id: json['id'],
      taskId: json['task_id'],
      imageUrl: json['image_url'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
```

### 4.4 创建lib/models/model.dart
```dart
class AIModel {
  final int id;
  final String name;
  final String displayName;
  final String description;
  
  AIModel({
    required this.id,
    required this.name,
    required this.displayName,
    required this.description,
  });
  
  factory AIModel.fromJson(Map<String, dynamic> json) {
    return AIModel(
      id: json['id'],
      name: json['name'],
      displayName: json['display_name'],
      description: json['description'],
    );
  }
}
```

---

## 🔌 第五步：创建API服务

### 5.1 创建lib/services/api_service.dart
```dart
import 'package:dio/dio.dart';
import 'package:image_gen_app/config/api_config.dart';
import 'package:logger/logger.dart';

class ApiService {
  late Dio _dio;
  final logger = Logger();
  
  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.baseUrl,
        connectTimeout: Duration(milliseconds: ApiConfig.connectTimeout),
        receiveTimeout: Duration(milliseconds: ApiConfig.receiveTimeout),
        contentType: 'application/json',
      ),
    );
    
    // 添加日志拦截器
    _dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        logPrint: (obj) => logger.d(obj),
      ),
    );
  }
  
  // GET请求
  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.get(
        path,
        queryParameters: queryParameters,
      );
      return fromJson != null ? fromJson(response.data) : response.data;
    } catch (e) {
      logger.e('GET $path failed: $e');
      rethrow;
    }
  }
  
  // POST请求
  Future<T> post<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.post(path, data: data);
      return fromJson != null ? fromJson(response.data) : response.data;
    } catch (e) {
      logger.e('POST $path failed: $e');
      rethrow;
    }
  }
  
  // PUT请求
  Future<T> put<T>(
    String path, {
    dynamic data,
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.put(path, data: data);
      return fromJson != null ? fromJson(response.data) : response.data;
    } catch (e) {
      logger.e('PUT $path failed: $e');
      rethrow;
    }
  }
  
  // DELETE请求
  Future<T> delete<T>(
    String path, {
    T Function(dynamic)? fromJson,
  }) async {
    try {
      final response = await _dio.delete(path);
      return fromJson != null ? fromJson(response.data) : response.data;
    } catch (e) {
      logger.e('DELETE $path failed: $e');
      rethrow;
    }
  }
  
  // 设置认证Token
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }
  
  // 清除认证Token
  void clearAuthToken() {
    _dio.options.headers.remove('Authorization');
  }
}
```

---

## 📱 第六步：创建主应用

### 6.1 创建lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:image_gen_app/config/app_theme.dart';
import 'package:image_gen_app/services/api_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiService>(create: (_) => ApiService()),
      ],
      child: MaterialApp(
        title: 'ImageGen',
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        home: const HomeScreen(),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ImageGen'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Welcome to ImageGen'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('App is ready!')),
                );
              },
              child: const Text('Get Started'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## ✅ 第七步：验证安装

### 7.1 检查Flutter环境
```bash
flutter doctor
```

### 7.2 运行应用
```bash
# 获取依赖
flutter pub get

# 运行应用
flutter run

# 或指定设备
flutter run -d chrome  # Web
flutter run -d emulator-5554  # Android模拟器
```

### 7.3 验证应用
- [ ] 应用启动成功
- [ ] 主页面显示正常
- [ ] 按钮可点击
- [ ] 没有编译错误

---

## 📊 检查清单

完成以下检查：
- [ ] Flutter项目创建完成
- [ ] 项目目录结构创建完成
- [ ] pubspec.yaml配置完成
- [ ] 所有依赖安装完成
- [ ] 配置文件创建完成
- [ ] 基础模型创建完成
- [ ] API服务创建完成
- [ ] 主应用创建完成
- [ ] 应用可编译运行
- [ ] 没有编译错误

---

## 🎯 完成标志

✅ 前端项目结构完成
✅ 所有依赖安装完成
✅ 基础框架创建完成
✅ 应用可编译运行
✅ 没有编译错误

**下一步**：数据库初始化和ComfyUI部署


