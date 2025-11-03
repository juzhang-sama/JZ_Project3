import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../models/generation_task.dart';
import '../providers/auth_provider.dart';

class GenerationScreen extends StatefulWidget {
  const GenerationScreen({Key? key}) : super(key: key);

  @override
  State<GenerationScreen> createState() => _GenerationScreenState();
}

class _GenerationScreenState extends State<GenerationScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _promptController = TextEditingController();

  String? _selectedModel;
  List<dynamic> _models = [];
  bool _isLoading = false;
  String? _generatedImageUrl;
  GenerationTask? _currentTask;
  double _progress = 0.0;
  String _progressStatus = '';
  List<GenerationTask> _taskHistory = [];

  @override
  void initState() {
    super.initState();
    _loadModels();
  }

  Future<void> _loadModels() async {
    try {
      final models = await _apiService.getModels();
      setState(() {
        _models = models;
        if (models.isNotEmpty) {
          _selectedModel = models[0]['name'];
        }
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load models: $e')),
      );
    }
  }

  Future<void> _generateImage() async {
    if (_promptController.text.isEmpty || _selectedModel == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter prompt and select model')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _generatedImageUrl = null;
      _progress = 0.0;
      _progressStatus = '初始化...';
    });

    try {
      // 使用异步API创建任务
      final result = await _apiService.createGenerationTaskAsync(
        prompt: _promptController.text,
        modelName: _selectedModel!,
      );

      setState(() {
        _currentTask = GenerationTask.fromJson(result);
        _progress = 0.1;
        _progressStatus = '任务已创建，等待处理...';
      });

      // 轮询任务状态
      _pollTaskStatus(_currentTask!.id);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to generate image: $e')),
      );
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _pollTaskStatus(int taskId) async {
    int pollCount = 0;
    while (_isLoading && _currentTask?.status != 'completed' && _currentTask?.status != 'failed') {
      await Future.delayed(const Duration(seconds: 1));
      pollCount++;

      try {
        final status = await _apiService.getTaskStatus(taskId);
        setState(() {
          _currentTask = GenerationTask.fromJson(status);

          // 更新进度
          if (_currentTask!.isProcessing) {
            _progress = 0.3 + (pollCount * 0.01).clamp(0.0, 0.8);
            _progressStatus = '正在生成图像...';
          } else if (_currentTask!.isPending) {
            _progress = 0.1 + (pollCount * 0.005).clamp(0.0, 0.3);
            _progressStatus = '等待处理中...';
          }
        });

        if (_currentTask!.isCompleted) {
          final result = await _apiService.getTaskResult(taskId);
          setState(() {
            _generatedImageUrl = result['image_url'];
            _isLoading = false;
            _progress = 1.0;
            _progressStatus = '完成！';
            _taskHistory.insert(0, _currentTask!);
          });
        } else if (_currentTask!.isFailed) {
          setState(() {
            _isLoading = false;
            _progress = 0.0;
            _progressStatus = '失败';
          });
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Generation failed: ${_currentTask!.errorMessage}')),
          );
        }
      } catch (e) {
        print('Poll status error: $e');
      }
    }
  }

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ImageGen - AI Image Generation'),
        actions: [
          Consumer<AuthProvider>(
            builder: (context, authProvider, _) {
              return PopupMenuButton<String>(
                onSelected: (value) async {
                  if (value == 'logout') {
                    await authProvider.logout();
                    if (mounted) {
                      Navigator.of(context).pushReplacementNamed('/login');
                    }
                  }
                },
                itemBuilder: (BuildContext context) => [
                  PopupMenuItem<String>(
                    enabled: false,
                    child: Text(
                      authProvider.currentUser?['username'] ?? 'User',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ),
                  const PopupMenuDivider(),
                  const PopupMenuItem<String>(
                    value: 'logout',
                    child: Text('登出'),
                  ),
                ],
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: CircleAvatar(
                    child: Text(
                      (authProvider.currentUser?['username'] ?? 'U')[0]
                          .toUpperCase(),
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 提示词输入
            TextField(
              controller: _promptController,
              decoration: InputDecoration(
                labelText: 'Enter your prompt',
                hintText: 'e.g., A beautiful sunset over mountains',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                enabled: !_isLoading,
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),

            // 模型选择
            DropdownButton<String>(
              value: _selectedModel,
              isExpanded: true,
              items: _models.map((model) {
                return DropdownMenuItem<String>(
                  value: model['name'],
                  child: Text(model['display_name'] ?? model['name']),
                );
              }).toList(),
              onChanged: _isLoading ? null : (value) {
                setState(() {
                  _selectedModel = value;
                });
              },
            ),
            const SizedBox(height: 16),

            // 生成按钮
            ElevatedButton(
              onPressed: _isLoading ? null : _generateImage,
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Generate Image'),
              ),
            ),
            const SizedBox(height: 24),

            // 进度显示
            if (_isLoading)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Generation Progress',
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          Text('${(_progress * 100).toStringAsFixed(0)}%'),
                        ],
                      ),
                      const SizedBox(height: 12),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: _progress,
                          minHeight: 8,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        _progressStatus,
                        style: const TextStyle(
                          fontSize: 14,
                          color: Colors.grey,
                        ),
                      ),
                      if (_currentTask != null) ...[
                        const SizedBox(height: 12),
                        Text(
                          'Status: ${_currentTask!.status}',
                          style: const TextStyle(fontSize: 12),
                        ),
                      ],
                    ],
                  ),
                ),
              ),

            // 任务状态卡片
            if (_currentTask != null && !_isLoading)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            _currentTask!.isCompleted
                                ? Icons.check_circle
                                : _currentTask!.isFailed
                                    ? Icons.cancel
                                    : Icons.info,
                            color: _currentTask!.isCompleted
                                ? Colors.green
                                : _currentTask!.isFailed
                                    ? Colors.red
                                    : Colors.blue,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'Status: ${_currentTask!.status}',
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text('Created: ${_currentTask!.createdAt}'),
                      if (_currentTask!.completedAt != null)
                        Text('Completed: ${_currentTask!.completedAt}'),
                      if (_currentTask!.errorMessage != null)
                        Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: Text(
                            'Error: ${_currentTask!.errorMessage}',
                            style: const TextStyle(color: Colors.red),
                          ),
                        ),
                    ],
                  ),
                ),
              ),

            // 生成的图片
            if (_generatedImageUrl != null)
              Padding(
                padding: const EdgeInsets.only(top: 16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Generated Image:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(
                        _generatedImageUrl!,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ],
                ),
              ),

            // 任务历史
            if (_taskHistory.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Recent Tasks',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 12),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: _taskHistory.length,
                      itemBuilder: (context, index) {
                        final task = _taskHistory[index];
                        return Card(
                          child: ListTile(
                            leading: Icon(
                              task.isCompleted
                                  ? Icons.check_circle
                                  : task.isFailed
                                      ? Icons.cancel
                                      : Icons.schedule,
                              color: task.isCompleted
                                  ? Colors.green
                                  : task.isFailed
                                      ? Colors.red
                                      : Colors.orange,
                            ),
                            title: Text(
                              task.prompt.length > 50
                                  ? '${task.prompt.substring(0, 50)}...'
                                  : task.prompt,
                            ),
                            subtitle: Text(task.status),
                            trailing: Text(task.modelName),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}

