import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:image_gen_app/services/auth_service.dart';

// Mock classes
class MockDio extends Mock implements Dio {}
class MockFlutterSecureStorage extends Mock implements FlutterSecureStorage {}

void main() {
  group('AuthService Tests', () {
    late AuthService authService;
    late MockDio mockDio;
    late MockFlutterSecureStorage mockStorage;

    setUp(() {
      mockDio = MockDio();
      mockStorage = MockFlutterSecureStorage();
      authService = AuthService();
      // Replace internal Dio and storage with mocks
      authService._dio = mockDio;
      authService._storage = mockStorage;
    });

    group('Register', () {
      test('register_success - should return user data on successful registration', () async {
        // Arrange
        final responseData = {
          'id': 1,
          'username': 'testuser',
          'email': 'test@example.com',
        };
        
        when(mockDio.post(
          '/register',
          data: anyNamed('data'),
        )).thenAnswer((_) async => Response(
          data: responseData,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/register'),
        ));

        // Act
        final result = await authService.register(
          username: 'testuser',
          email: 'test@example.com',
          password: 'password12345',
        );

        // Assert
        expect(result['username'], equals('testuser'));
        expect(result['email'], equals('test@example.com'));
        verify(mockDio.post(
          '/register',
          data: anyNamed('data'),
        )).called(1);
      });

      test('register_failure - should throw exception on registration failure', () async {
        // Arrange
        when(mockDio.post(
          '/register',
          data: anyNamed('data'),
        )).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/register'),
          error: 'Registration failed',
        ));

        // Act & Assert
        expect(
          () => authService.register(
            username: 'testuser',
            email: 'test@example.com',
            password: 'password12345',
          ),
          throwsA(isA<DioException>()),
        );
      });
    });

    group('Login', () {
      test('login_success - should save tokens and return user data', () async {
        // Arrange
        final responseData = {
          'access_token': 'access_token_123',
          'refresh_token': 'refresh_token_456',
          'token_type': 'bearer',
        };
        
        when(mockDio.post(
          '/login',
          data: anyNamed('data'),
        )).thenAnswer((_) async => Response(
          data: responseData,
          statusCode: 200,
          requestOptions: RequestOptions(path: '/login'),
        ));

        when(mockStorage.write(
          key: anyNamed('key'),
          value: anyNamed('value'),
        )).thenAnswer((_) async => null);

        // Act
        final result = await authService.login(
          email: 'test@example.com',
          password: 'password12345',
        );

        // Assert
        expect(result['access_token'], equals('access_token_123'));
        expect(result['refresh_token'], equals('refresh_token_456'));
        verify(mockStorage.write(
          key: 'access_token',
          value: 'access_token_123',
        )).called(1);
        verify(mockStorage.write(
          key: 'refresh_token',
          value: 'refresh_token_456',
        )).called(1);
      });

      test('login_failure - should throw exception on login failure', () async {
        // Arrange
        when(mockDio.post(
          '/login',
          data: anyNamed('data'),
        )).thenThrow(DioException(
          requestOptions: RequestOptions(path: '/login'),
          error: 'Invalid credentials',
        ));

        // Act & Assert
        expect(
          () => authService.login(
            email: 'test@example.com',
            password: 'wrongpassword',
          ),
          throwsA(isA<DioException>()),
        );
      });
    });

    group('Logout', () {
      test('logout_success - should clear tokens', () async {
        // Arrange
        when(mockStorage.read(key: 'access_token'))
            .thenAnswer((_) async => 'access_token_123');
        when(mockDio.post(
          '/logout',
          options: anyNamed('options'),
        )).thenAnswer((_) async => Response(
          data: {},
          statusCode: 200,
          requestOptions: RequestOptions(path: '/logout'),
        ));
        when(mockStorage.delete(key: anyNamed('key')))
            .thenAnswer((_) async => null);

        // Act
        await authService.logout();

        // Assert
        verify(mockStorage.delete(key: 'access_token')).called(1);
        verify(mockStorage.delete(key: 'refresh_token')).called(1);
      });
    });

    group('IsLoggedIn', () {
      test('isLoggedIn_true - should return true when token exists', () async {
        // Arrange
        when(mockStorage.read(key: 'access_token'))
            .thenAnswer((_) async => 'access_token_123');

        // Act
        final result = await authService.isLoggedIn();

        // Assert
        expect(result, isTrue);
      });

      test('isLoggedIn_false - should return false when token does not exist', () async {
        // Arrange
        when(mockStorage.read(key: 'access_token'))
            .thenAnswer((_) async => null);

        // Act
        final result = await authService.isLoggedIn();

        // Assert
        expect(result, isFalse);
      });
    });
  });
}

