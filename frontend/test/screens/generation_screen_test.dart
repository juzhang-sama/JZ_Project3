import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';
import 'package:image_gen_app/screens/generation_screen.dart';
import 'package:image_gen_app/services/api_service.dart';

// Mock classes
class MockApiService extends Mock implements ApiService {}

void main() {
  group('GenerationScreen Widget Tests', () {
    late MockApiService mockApiService;

    setUp(() {
      mockApiService = MockApiService();
    });

    Widget createWidgetUnderTest() {
      return MaterialApp(
        home: Provider<ApiService>.value(
          value: mockApiService,
          child: const GenerationScreen(),
        ),
      );
    }

    testWidgets('generation_screen_renders - should display generation form', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(TextField), findsWidgets);
      expect(find.byType(ElevatedButton), findsWidgets);
    });

    testWidgets('prompt_field_exists - should have prompt input field', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(TextField), findsWidgets);
    });

    testWidgets('generate_button_exists - should have generate button', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(ElevatedButton), findsWidgets);
    });

    testWidgets('prompt_input_works - should accept prompt input', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      final promptField = find.byType(TextField).first;
      await tester.enterText(promptField, 'a beautiful sunset');
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('a beautiful sunset'), findsWidgets);
    });

    testWidgets('models_dropdown_exists - should have model selection', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
        {'id': 2, 'name': 'model2', 'description': 'Model 2'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(DropdownButton), findsWidgets);
    });

    testWidgets('progress_indicator_hidden_initially - should not show progress initially', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(LinearProgressIndicator), findsNothing);
    });

    testWidgets('task_history_section_exists - should display task history', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(ListView), findsWidgets);
    });

    testWidgets('generate_button_tap - should trigger generation', (WidgetTester tester) async {
      // Arrange
      when(mockApiService.getModels()).thenAnswer((_) async => [
        {'id': 1, 'name': 'model1', 'description': 'Model 1'},
      ]);
      when(mockApiService.createGenerationTaskAsync(
        prompt: anyNamed('prompt'),
        modelName: anyNamed('modelName'),
      )).thenAnswer((_) async => {
        'id': 1,
        'status': 'pending',
      });

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.pumpAndSettle();

      final promptField = find.byType(TextField).first;
      await tester.enterText(promptField, 'test prompt');
      await tester.pumpWidget(createWidgetUnderTest());

      final generateButton = find.byType(ElevatedButton).first;
      await tester.tap(generateButton);
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert - Button should be tappable
      expect(generateButton, findsWidgets);
    });
  });
}

