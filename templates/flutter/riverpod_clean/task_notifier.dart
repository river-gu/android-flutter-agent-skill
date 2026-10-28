import 'package:flutter_riverpod/flutter_riverpod.dart';

class TaskItem {
  final String id;
  final String name;
  final bool isDone;
  const TaskItem({required this.id, required this.name, this.isDone = false});

  TaskItem copyWith({bool? isDone}) =>
      TaskItem(id: id, name: name, isDone: isDone ?? this.isDone);
}

class TaskListNotifier extends AsyncNotifier<List<TaskItem>> {
  @override
  Future<List<TaskItem>> build() async {
    // Initial fetch
    await Future.delayed(const Duration(milliseconds: 300));
    return [
      const TaskItem(id: '1', name: 'Riverpod 2.x State Management'),
      const TaskItem(id: '2', name: 'AsyncNotifier Pattern'),
    ];
  }

  Future<void> toggle(String id) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final current = state.value ?? [];
      return current.map((t) => t.id == id ? t.copyWith(isDone: !t.isDone) : t).toList();
    });
  }
}

final taskListProvider =
    AsyncNotifierProvider<TaskListNotifier, List<TaskItem>>(TaskListNotifier.new);
