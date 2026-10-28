import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:task_app/features/task/task_bloc.dart';

void main() {
  group('TaskBloc Tests', () {
    late TaskBloc taskBloc;

    setUp(() {
      taskBloc = TaskBloc();
    });

    tearDown(() {
      taskBloc.close();
    });

    test('initial state is TaskInitial', () {
      expect(taskBloc.state, isA<TaskInitial>());
    });

    blocTest<TaskBloc, TaskState>(
      'emits [TaskLoading, TaskSuccess] when TaskRequested is added',
      build: () => taskBloc,
      act: (bloc) => bloc.add(TaskRequested()),
      expect: () => [
        isA<TaskLoading>(),
        isA<TaskSuccess>().having(
          (state) => state.tasks.length,
          'tasks count',
          2,
        ),
      ],
    );

    blocTest<TaskBloc, TaskState>(
      'toggles task completion when TaskToggled is added',
      build: () => taskBloc,
      seed: () => TaskSuccess([
        const Task(id: '1', title: 'Test Task', isCompleted: false),
      ]),
      act: (bloc) => bloc.add(TaskToggled('1')),
      expect: () => [
        isA<TaskSuccess>().having(
          (state) => state.tasks.first.isCompleted,
          'task is completed',
          true,
        ),
      ],
    );
  });
}
