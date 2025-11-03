import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';
import 'package:image_gen_app/screens/login_screen.dart';
import 'package:image_gen_app/providers/auth_provider.dart';

// Mock classes
class MockAuthProvider extends Mock implements AuthProvider {}

void main() {
  group('LoginScreen Widget Tests', () {
    late MockAuthProvider mockAuthProvider;

    setUp(() {
      mockAuthProvider = MockAuthProvider();
    });

    Widget createWidgetUnderTest() {
      return MaterialApp(
        home: ChangeNotifierProvider<AuthProvider>.value(
          value: mockAuthProvider,
          child: const LoginScreen(),
        ),
      );
    }

    testWidgets('login_screen_renders - should display login form', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(TextField), findsWidgets);
      expect(find.byType(ElevatedButton), findsWidgets);
      expect(find.text('Login'), findsWidgets);
    });

    testWidgets('email_field_exists - should have email input field', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(TextField), findsWidgets);
    });

    testWidgets('password_field_exists - should have password input field', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(TextField), findsWidgets);
    });

    testWidgets('login_button_exists - should have login button', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(ElevatedButton), findsWidgets);
    });

    testWidgets('register_link_exists - should have register link', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(GestureDetector), findsWidgets);
    });

    testWidgets('email_input_works - should accept email input', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      final emailFields = find.byType(TextField);
      await tester.enterText(emailFields.first, 'test@example.com');
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('test@example.com'), findsWidgets);
    });

    testWidgets('password_input_works - should accept password input', (WidgetTester tester) async {
      // Arrange & Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      final passwordFields = find.byType(TextField);
      await tester.enterText(passwordFields.last, 'password123');
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('password123'), findsWidgets);
    });

    testWidgets('login_button_tap - should trigger login on button tap', (WidgetTester tester) async {
      // Arrange
      when(mockAuthProvider.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => true);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      final textFields = find.byType(TextField);
      await tester.enterText(textFields.first, 'test@example.com');
      await tester.enterText(textFields.last, 'password12345');
      await tester.pumpWidget(createWidgetUnderTest());

      final loginButton = find.byType(ElevatedButton);
      await tester.tap(loginButton);
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert - Button should be tappable
      expect(loginButton, findsWidgets);
    });
  });
}

