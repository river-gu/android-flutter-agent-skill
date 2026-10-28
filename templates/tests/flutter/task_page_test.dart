import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:task_app/features/task/task_page.dart';

void main() {
  group('TaskPage Widget Tests', () {
    testWidgets('renders AppBar and initial loading indicator', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: TaskPage(),
        ),
      );

      // Verify AppBar title
      expect(find.text('Flutter Task Manager'), findsOneWidget);

      // Verify CircularProgressIndicator is displayed during load
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // Let mock timer complete
      await tester.pumpAndSettle();

      // Verify loaded tasks
      expect(find.text('Implement BLoC Pattern'), findsOneWidget);
      expect(find.text('Write Widget Tests'), findsOneWidget);
      expect(find.byType(Checkbox), findsNWidgets(2));
    });

    testWidgets('toggles checkbox when clicked', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: TaskPage(),
        ),
      );
      await tester.pumpAndSettle();

      // Find first checkbox
      final firstCheckbox = find.byType(Checkbox).first;
      Checkbox checkboxWidget = tester.widget(firstCheckbox);
      expect(checkboxWidget.value, isFalse);

      // Tap checkbox
      await tester.tap(firstCheckbox);
      await tester.pumpAndSettle();

      // Verify state updated to true
      checkboxWidget = tester.widget(firstCheckbox);
      expect(checkboxWidget.value, isTrue);
    });
  });
}
