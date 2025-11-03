# ImageGen Frontend

Flutter 前端应用

## 快速启动

### 1. 创建项目

```bash
flutter create image_gen_app
cd image_gen_app
```

### 2. 获取依赖

```bash
flutter pub get
```

### 3. 运行应用

```bash
# 运行到默认设备
flutter run

# 运行到特定设备
flutter run -d chrome      # Web
flutter run -d emulator-5554  # Android模拟器
```

## 项目结构

```
lib/
├── main.dart              # 应用入口
├── config/
│   ├── api_config.dart    # API配置
│   └── app_theme.dart     # 主题配置
├── screens/               # 页面
│   ├── auth/
│   ├── home/
│   ├── generate/
│   ├── result/
│   └── profile/
├── providers/             # 状态管理
├── services/              # 服务
├── models/                # 数据模型
├── widgets/               # 组件
└── utils/                 # 工具函数
```

## 开发

### 代码格式化

```bash
dart format lib/
```

### 代码分析

```bash
dart analyze
```

### 运行测试

```bash
flutter test
```

## 构建

### Android

```bash
flutter build apk
```

### iOS

```bash
flutter build ios
```

### Web

```bash
flutter build web
```

## 常见问题

### 依赖冲突

```bash
flutter clean
flutter pub get
```

### 编译错误

```bash
flutter doctor
flutter pub upgrade
```

## 许可证

MIT

