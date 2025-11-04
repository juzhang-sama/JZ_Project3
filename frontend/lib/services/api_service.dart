/// API服务
import 'package:dio/dio.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.18.2:8001/api/v1';
  late Dio _dio;

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );

    // 添加日志拦截器
    _dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
      ),
    );
  }

  /// 健康检查
  Future<bool> healthCheck() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  /// 获取模型列表
  Future<List<dynamic>> getModels() async {
    try {
      final response = await _dio.get('/models');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Get models failed: $e');
      rethrow;
    }
  }

  /// 创建生成任务
  Future<Map<String, dynamic>> createGenerationTask({
    required String prompt,
    required String modelName,
  }) async {
    try {
      final response = await _dio.post(
        '/generation/create',
        data: {
          'prompt': prompt,
          'model_name': modelName,
        },
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      print('Create generation task failed: $e');
      rethrow;
    }
  }

  /// 创建异步生成任务
  Future<Map<String, dynamic>> createGenerationTaskAsync({
    required String prompt,
    required String modelName,
  }) async {
    try {
      final response = await _dio.post(
        '/generation/create-async',
        data: {
          'prompt': prompt,
          'model_name': modelName,
        },
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      print('Create async generation task failed: $e');
      rethrow;
    }
  }

  /// 获取任务状态
  Future<Map<String, dynamic>> getTaskStatus(int taskId) async {
    try {
      final response = await _dio.get('/generation/status/$taskId');
      return response.data as Map<String, dynamic>;
    } catch (e) {
      print('Get task status failed: $e');
      rethrow;
    }
  }

  /// 获取任务结果
  Future<Map<String, dynamic>> getTaskResult(int taskId) async {
    try {
      final response = await _dio.get('/generation/result/$taskId');
      return response.data as Map<String, dynamic>;
    } catch (e) {
      print('Get task result failed: $e');
      rethrow;
    }
  }

  /// 获取历史记录
  Future<List<dynamic>> getHistory({int page = 1, int pageSize = 10}) async {
    try {
      final response = await _dio.get(
        '/generation/history',
        queryParameters: {
          'page': page,
          'page_size': pageSize,
        },
      );
      return response.data as List<dynamic>;
    } catch (e) {
      print('Get history failed: $e');
      rethrow;
    }
  }
}

