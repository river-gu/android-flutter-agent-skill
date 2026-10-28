# Modern Flutter & Dart Guidelines

## 一、核心技术栈推荐 (2025 - 2026)

- **框架与语言**：Flutter 3.22+, Dart 3.4+ (充分利用 Pattern Matching, Records, Class Modifiers)
- **状态管理**：`flutter_bloc` 8.x (大型/企业级规范) 或 `flutter_riverpod` 2.x (现代化响应式)
- **网络与序列化**：`dio` 5.x, `retrofit` (或原生 Dio 封装), `freezed` + `json_serializable`
- **本地存储**：`flutter_secure_storage` (敏感凭据), `isar` / `hive_ce` / `drift` (结构化数据)
- **路由管理**：`go_router` 14.x (声明式路由、深链接、类型安全路由)

---

## 二、Dart 3 现代语言特性规范

### 1. 模式匹配与密封类 (Pattern Matching & Sealed Classes)
Dart 3 引入了原生的 `sealed class`，是实现 UI State 和 Event 的首选：
```dart
sealed class TaskState {}

final class TaskInitial extends TaskState {}
final class TaskLoading extends TaskState {}
final class TaskSuccess extends TaskState {
  final List<Task> tasks;
  const TaskSuccess(this.tasks);
}
final class TaskError extends TaskState {
  final String message;
  const TaskError(this.message);
}

// 消费端支持穷举检查 (Exhaustiveness checking)
Widget buildView(BuildContext context, TaskState state) {
  return switch (state) {
    TaskInitial() || TaskLoading() => const CircularProgressIndicator(),
    TaskSuccess(:final tasks) => TaskListView(tasks: tasks),
    TaskError(:final message) => ErrorBanner(message: message),
  };
}
```

---

## 三、Flutter 性能与架构守则

### 1. 恒定构造函数 (const Constructors)
- 尽可能对 StatelessWidget 和不可变子树添加 `const`。这使得 Flutter 能够跳过该子树的重新构建，极大降低丢帧率。

### 2. 精确颗粒度的状态重建
- 避免在整个页面根节点使用 `setState()` 或顶层 `BlocBuilder`。
- 将状态监听器下沉到具体的局部组件，例如只在购物车角标或单个 ListTile 内部监听状态。
```dart
// ✅ 推荐：仅局部重建数量文本
Widget buildBadge(BuildContext context) {
  return BlocSelector<CartBloc, CartState, int>(
    selector: (state) => state.totalItems,
    builder: (context, count) => Text('$count'),
  );
}
```

### 3. 内存泄漏防范
- 每一个 `AnimationController`、`TextEditingController`、`ScrollController`、`StreamSubscription` 必须在 `State.dispose()` 中显式释放。
- 在 `CustomPainter` 或图像处理中，及时调用 `Picture.dispose()` 与 `Image.dispose()`。
