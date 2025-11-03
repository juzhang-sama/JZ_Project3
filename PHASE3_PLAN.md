# 第三阶段规划：生成功能开发

**阶段**：第三阶段
**预计工时**：35小时
**预计周期**：1周
**状态**：⏳ 待执行

---

## 📋 阶段目标

实现完整的AI图像生成功能，包括：
- ✅ 生成任务创建
- ✅ 任务状态查询
- ✅ 结果获取
- ✅ 前端生成UI
- ✅ ComfyUI集成

---

## 🎯 核心功能

### 1. 生成任务API（8小时）
**后端**：
- POST /api/v1/generation/create - 创建生成任务
- GET /api/v1/generation/status/{task_id} - 获取任务状态
- GET /api/v1/generation/result/{task_id} - 获取任务结果
- GET /api/v1/generation/history - 获取生成历史
- DELETE /api/v1/generation/{task_id} - 删除任务

**功能**：
- 任务验证
- 数据库存储
- 状态管理
- 错误处理

### 2. ComfyUI集成（10小时）
**后端**：
- ComfyUI服务类
- 工作流生成
- 任务提交
- 结果获取
- 错误处理

**功能**：
- 连接ComfyUI API
- 生成工作流
- 提交任务
- 轮询结果
- 保存结果

### 3. 异步任务处理（8小时）
**后端**：
- Celery任务队列
- 后台处理
- 任务监控
- 结果回调

**功能**：
- 异步生成
- 进度跟踪
- 错误重试
- 超时处理

### 4. 前端生成UI（7小时）
**前端**：
- 生成页面优化
- 进度显示
- 结果展示
- 历史记录

**功能**：
- 提示词输入
- 模型选择
- 参数调整
- 结果预览

### 5. 前后端集成（2小时）
**集成**：
- API调用
- 错误处理
- 状态同步
- 用户反馈

---

## 📊 任务分解

### 后端任务

#### Task 1: ComfyUI服务（5小时）
- [ ] 创建ComfyUI客户端
- [ ] 实现工作流生成
- [ ] 实现任务提交
- [ ] 实现结果获取

#### Task 2: 生成API（5小时）
- [ ] 实现创建任务接口
- [ ] 实现查询状态接口
- [ ] 实现获取结果接口
- [ ] 实现历史记录接口

#### Task 3: 异步处理（5小时）
- [ ] 配置Celery
- [ ] 创建异步任务
- [ ] 实现进度跟踪
- [ ] 实现错误处理

### 前端任务

#### Task 4: 生成页面优化（3小时）
- [ ] 优化UI布局
- [ ] 添加参数控制
- [ ] 添加进度显示
- [ ] 添加结果预览

#### Task 5: 历史记录（2小时）
- [ ] 创建历史页面
- [ ] 实现列表显示
- [ ] 实现删除功能
- [ ] 实现详情查看

#### Task 6: 前后端集成（2小时）
- [ ] 集成API调用
- [ ] 实现错误处理
- [ ] 实现状态同步
- [ ] 测试完整流程

---

## 📁 文件结构

### 后端新增文件
```
backend/app/
├── services/
│   ├── __init__.py
│   ├── comfyui_service.py      # ComfyUI服务
│   └── generation_service.py   # 生成服务
├── api/
│   └── generation.py           # 生成API
├── tasks/
│   ├── __init__.py
│   └── generation_tasks.py     # 异步任务
└── utils/
    └── comfyui_workflow.py     # 工作流生成
```

### 前端新增文件
```
frontend/lib/
├── screens/
│   ├── generation_screen.dart  # 更新
│   ├── history_screen.dart     # 历史记录
│   └── result_screen.dart      # 结果详情
├── widgets/
│   ├── progress_indicator.dart # 进度指示
│   └── image_preview.dart      # 图片预览
└── models/
    └── generation_result.dart  # 结果模型
```

---

## 🔧 技术实现

### ComfyUI工作流
```python
# 基础工作流结构
{
    "1": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "model_name"}
    },
    "2": {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": "prompt", "clip": ["1", 0]}
    },
    # ... 更多节点
}
```

### 异步任务
```python
@celery_app.task
def generate_image(task_id, prompt, model_name):
    # 生成图像
    # 保存结果
    # 更新任务状态
    pass
```

### 前端轮询
```dart
// 轮询任务状态
Timer.periodic(Duration(seconds: 2), (timer) {
  // 查询任务状态
  // 更新UI
  // 完成时停止轮询
});
```

---

## 📈 验收标准

### 后端验收
- [ ] ComfyUI连接正常
- [ ] 工作流生成正确
- [ ] 任务创建成功
- [ ] 状态查询正常
- [ ] 结果获取正确
- [ ] 异步处理工作
- [ ] 错误处理完善

### 前端验收
- [ ] 生成页面可用
- [ ] 进度显示正常
- [ ] 结果预览正确
- [ ] 历史记录显示
- [ ] 错误提示清晰
- [ ] 用户体验良好

---

## 🚀 快速启动

### 启动ComfyUI
```bash
cd ComfyUI
python main.py
```

### 启动后端
```bash
cd backend
source venv/bin/activate
celery -A app.tasks worker --loglevel=info
uvicorn app.main:app --reload
```

### 启动前端
```bash
cd frontend
flutter run
```

---

## 📝 下一步

1. ✅ 创建ComfyUI服务
2. ✅ 创建生成API
3. ✅ 配置异步任务
4. ✅ 优化前端UI
5. ✅ 集成前后端
6. ✅ 完整测试

---

**预计完成时间**：1周
**优先级**：高
**依赖**：第二阶段完成、ComfyUI部署

