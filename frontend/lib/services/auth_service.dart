import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  static const String baseUrl = 'http://192.168.18.2:8000/api/v1/auth';
  late Dio _dio;
  final _storage = const FlutterSecureStorage();

  AuthService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
  }

  /// 用户注册
  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/register',
        data: {
          'username': username,
          'email': email,
          'password': password,
        },
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      rethrow;
    }
  }

  /// 用户登录
  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      final data = response.data as Map<String, dynamic>;
      
      // 保存令牌
      await _storage.write(
        key: 'access_token',
        value: data['access_token'],
      );
      await _storage.write(
        key: 'refresh_token',
        value: data['refresh_token'],
      );

      return data;
    } catch (e) {
      rethrow;
    }
  }

  /// 获取当前用户信息
  Future<Map<String, dynamic>> getCurrentUser() async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) {
        throw Exception('No access token found');
      }

      final response = await _dio.get(
        '/me',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );

      return response.data as Map<String, dynamic>;
    } catch (e) {
      rethrow;
    }
  }

  /// 更新用户信息
  Future<Map<String, dynamic>> updateProfile({
    String? username,
    String? avatarUrl,
  }) async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) {
        throw Exception('No access token found');
      }

      final data = <String, dynamic>{};
      if (username != null) data['username'] = username;
      if (avatarUrl != null) data['avatar_url'] = avatarUrl;

      final response = await _dio.put(
        '/profile',
        data: data,
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
          },
        ),
      );

      return response.data as Map<String, dynamic>;
    } catch (e) {
      rethrow;
    }
  }

  /// 刷新令牌
  Future<Map<String, dynamic>> refreshToken() async {
    try {
      final refreshToken = await _storage.read(key: 'refresh_token');
      if (refreshToken == null) {
        throw Exception('No refresh token found');
      }

      final response = await _dio.post(
        '/refresh',
        data: {
          'refresh_token': refreshToken,
        },
      );

      final data = response.data as Map<String, dynamic>;

      // 更新令牌
      await _storage.write(
        key: 'access_token',
        value: data['access_token'],
      );

      return data;
    } catch (e) {
      rethrow;
    }
  }

  /// 用户登出
  Future<void> logout() async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token != null) {
        await _dio.post(
          '/logout',
          options: Options(
            headers: {
              'Authorization': 'Bearer $token',
            },
          ),
        );
      }

      // 清除本地令牌
      await _storage.delete(key: 'access_token');
      await _storage.delete(key: 'refresh_token');
    } catch (e) {
      // 即使请求失败，也清除本地令牌
      await _storage.delete(key: 'access_token');
      await _storage.delete(key: 'refresh_token');
    }
  }

  /// 检查是否已登录
  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }

  /// 获取访问令牌
  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }
}

