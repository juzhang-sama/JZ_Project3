import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';
import 'package:image_gen_app/services/api_service.dart';

// Mock classes
class MockDio extends Mock implements Dio {}

void main() {
  group('ApiService Tests', () {
    late ApiService apiService;
    late MockDio mockDio;

    setUp(() {
      mockDio = MockDio();
      apiService = ApiService();
      // Replace internal Dio with mock
      apiService._dio = mockDio;
    });

    group('Health Check', () {
      test('healthCheck_success - should return true on successful health check', () async {
        // Arrange
        when(mockDio.get('/health')).thenAnswer((_) async => Response(
          data: {'status': 'ok'},
          statusCode: 200,
          requestOptions: RequestOptions(path: '/health'),
        ));

        // Act
        final result = await apiService.healthCheck();

        // Assert
        expect(result, isTrue);
        verify(mockDio.get('/health')).called(1);
      });

      test('healthCheck_failure - should return false on health check failure', () async {
        // Arrange
        when(mockDio.get('/health')).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/health'),
          error: 'Connection failed',
        ));

        // Act
        final result = await apiService.healthCheck();

        // Assert
        expect(result, isFalse);
      });
    });

    group('Get Models', () {
      test('getModels_success - should return list of models', () async {
        // Arrange
        final modelsList = [
          {'id': 1, 'name': 'model1', 'description': 'Model 1'},
          {'id': 2, 'name': 'model2', 'description': 'Model 2'},
        ];
        
        when(mockDio.get('/models')).thenAnswer((_) async => Response(
          data: modelsList,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/models'),
        ));

        // Act
        final result = await apiService.getModels();

        // Assert
        expect(result, isA<List>());
        expect(result.length, equals(2));
        expect(result[0]['name'], equals('model1'));
        verify(mockDio.get('/models')).called(1);
      });

      test('getModels_failure - should throw exception on failure', () async {
        // Arrange
        when(mockDio.get('/models')).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/models'),
          error: 'Failed to fetch models',
        ));

        // Act & Assert
        expect(
          () => apiService.getModels(),
          throwsA(isA<DioException>()),
        );
      });
    });

    group('Create Generation Task', () {
      test('createGenerationTask_success - should return task data', () async {
        // Arrange
        final taskData = {
          'id': 1,
          'prompt': 'test prompt',
          'model_name': 'model1',
          'status': 'completed',
        };
        
        when(mockDio.post(
          '/generation/create',
          data: anyNamed('data'),
        )).thenAnswer((_) async => Response(
          data: taskData,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/generation/create'),
        ));

        // Act
        final result = await apiService.createGenerationTask(
          prompt: 'test prompt',
          modelName: 'model1',
        );

        // Assert
        expect(result['id'], equals(1));
        expect(result['prompt'], equals('test prompt'));
        expect(result['status'], equals('completed'));
        verify(mockDio.post(
          '/generation/create',
          data: anyNamed('data'),
        )).called(1);
      });

      test('createGenerationTask_failure - should throw exception on failure', () async {
        // Arrange
        when(mockDio.post(
          '/generation/create',
          data: anyNamed('data'),
        )).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/generation/create'),
          error: 'Failed to create task',
        ));

        // Act & Assert
        expect(
          () => apiService.createGenerationTask(
            prompt: 'test prompt',
            modelName: 'model1',
          ),
          throwsA(isA<DioException>()),
        );
      });
    });

    group('Create Async Generation Task', () {
      test('createGenerationTaskAsync_success - should return task data', () async {
        // Arrange
        final taskData = {
          'id': 1,
          'prompt': 'test prompt',
          'model_name': 'model1',
          'status': 'pending',
        };
        
        when(mockDio.post(
          '/generation/create-async',
          data: anyNamed('data'),
        )).thenAnswer((_) async => Response(
          data: taskData,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/generation/create-async'),
        ));

        // Act
        final result = await apiService.createGenerationTaskAsync(
          prompt: 'test prompt',
          modelName: 'model1',
        );

        // Assert
        expect(result['id'], equals(1));
        expect(result['status'], equals('pending'));
        verify(mockDio.post(
          '/generation/create-async',
          data: anyNamed('data'),
        )).called(1);
      });
    });

    group('Get Task Status', () {
      test('getTaskStatus_success - should return task status', () async {
        // Arrange
        final statusData = {
          'id': 1,
          'status': 'completed',
          'progress': 100,
        };
        
        when(mockDio.get('/generation/status/1')).thenAnswer((_) async => Response(
          data: statusData,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/generation/status/1'),
        ));

        // Act
        final result = await apiService.getTaskStatus(1);

        // Assert
        expect(result['status'], equals('completed'));
        expect(result['progress'], equals(100));
        verify(mockDio.get('/generation/status/1')).called(1);
      });

      test('getTaskStatus_failure - should throw exception on failure', () async {
        // Arrange
        when(mockDio.get('/generation/status/1')).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/generation/status/1'),
          error: 'Task not found',
        ));

        // Act & Assert
        expect(
          () => apiService.getTaskStatus(1),
          throwsA(isA<DioException>()),
        );
      });
    });
  });
}

