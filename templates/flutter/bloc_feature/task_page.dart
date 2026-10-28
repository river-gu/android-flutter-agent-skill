import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'task_bloc.dart';

class TaskPage extends StatelessWidget {
  const TaskPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => TaskBloc()..add(TaskRequested()),
      child: Scaffold(
        appBar: AppBar(title: const Text('Flutter Task Manager')),
        body: BlocBuilder<TaskBloc, TaskState>(
          builder: (context, state) {
            return switch (state) {
              TaskInitial() || TaskLoading() =>
                const Center(child: CircularProgressIndicator()),
              TaskSuccess(:final tasks) => ListView.separated(
                  itemCount: tasks.length,
                  separatorBuilder: (_, __) => const Divider(),
                  itemBuilder: (context, index) {
                    final item = tasks[index];
                    return ListTile(
                      title: Text(item.title),
                      trailing: Checkbox(
                        value: item.isCompleted,
                        onChanged: (_) {
                          context.read<TaskBloc>().add(TaskToggled(item.id));
                        },
                      ),
                    );
                  },
                ),
              TaskFailure(:final message) => Center(
                  child: Text('Error: $message', style: const TextStyle(color: Colors.red)),
                ),
            };
          },
        ),
      ),
    );
  }
}
