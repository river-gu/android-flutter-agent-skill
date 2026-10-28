import 'package:flutter_bloc/flutter_bloc.dart';

// Model
class Task {
  final String id;
  final String title;
  final bool isCompleted;

  const Task({required this.id, required this.title, this.isCompleted = false});

  Task copyWith({bool? isCompleted}) {
    return Task(
      id: id,
      title: title,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}

// Events
sealed class TaskEvent {}
final class TaskRequested extends TaskEvent {}
final class TaskToggled extends TaskEvent {
  final String id;
  TaskToggled(this.id);
}

// States
sealed class TaskState {}
final class TaskInitial extends TaskState {}
final class TaskLoading extends TaskState {}
final class TaskSuccess extends TaskState {
  final List<Task> tasks;
  TaskSuccess(this.tasks);
}
final class TaskFailure extends TaskState {
  final String message;
  TaskFailure(this.message);
}

// Bloc
class TaskBloc extends Bloc<TaskEvent, TaskState> {
  TaskBloc() : super(TaskInitial()) {
    on<TaskRequested>(_onRequested);
    on<TaskToggled>(_onToggled);
  }

  Future<void> _onRequested(TaskRequested event, Emitter<TaskState> emit) async {
    emit(TaskLoading());
    try {
      await Future.delayed(const Duration(milliseconds: 400));
      emit(TaskSuccess([
        const Task(id: '1', title: 'Implement BLoC Pattern'),
        const Task(id: '2', title: 'Write Widget Tests'),
      ]));
    } catch (e) {
      emit(TaskFailure(e.toString()));
    }
  }

  void _onToggled(TaskToggled event, Emitter<TaskState> emit) {
    if (state is TaskSuccess) {
      final current = (state as TaskSuccess).tasks;
      final updated = current.map((t) {
        return t.id == event.id ? t.copyWith(isCompleted: !t.isCompleted) : t;
      }).toList();
      emit(TaskSuccess(updated));
    }
  }
}
