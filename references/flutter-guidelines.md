# Modern Flutter & Dart Guidelines

## 一、核心技术栈推荐 (2025 - 2026)

- **框架与语言**：Flutter 3.22+, Dart 3.4+ (充分利用 Pattern Matching, Records, Class Modifiers)。
- **状态管理**：`flutter_bloc` 8.x (大型/企业级首选) 或 `flutter_riverpod` 2.x (现代化响应式)。
- **网络与序列化**：`dio` 5.x + `retrofit` (或原生 Dio 拦截器封装), `freezed` + `json_serializable`。
- **本地存储**：`flutter_secure_storage` (敏感 Token 凭据), `isar` / `hive_ce` / `drift` (结构化数据)。
- **路由管理**：`go_router` 14.x (声明式路由、深链接、类型安全路由)。

---

## 二、核心操作守则与严格禁止项 (Negative Constraints)

在 Flutter / Dart 编码过程中，AI Agent 必须严格恪守以下禁止项：

1. ❌ **严禁跨 `await` 异步缝隙裸用 `BuildContext`**：
   - 在任何 `await` 异步调用之后，必须前置校验 `if (!context.mounted) return;` 才能使用 `Navigator`、`Theme.of` 或 `ScaffoldMessenger`，避免因页面退出导致异步回调调用失效 context 崩溃。
   ```dart
   // ❌ 错误示范
   await authRepository.login();
   Navigator.of(context).pushNamed('/home'); // 危险：页面可能已被销毁

   // ✅ 推荐合规
   await authRepository.login();
   if (!context.mounted) return;
   Navigator.of(context).pushNamed('/home');
   ```

2. ❌ **严禁 Controller / Stream 资源未释放造成内存泄漏**：
   - 所有的 `TextEditingController`、`ScrollController`、`AnimationController`、`StreamSubscription` 必须在 `State.dispose()` 中显式关闭，或在 `flutter_hooks` 中使用 `useTextEditingController` 自动管理。

3. ❌ **严禁在页面根节点滥用深层 `setState()`**：
   - 严禁为了更新一个文本或一个按钮状态而在包含长列表或大组件树的根节点调用 `setState()`。
   - 局部更新必须下沉到专有的小型 Widget，或使用 `BlocSelector` / `ValueNotifier` / `Consumer` 进行局部精准重绘。

4. ❌ **严禁在 `build()` 方法中实例化状态管理对象**：
   - 严禁在 `Widget.build()` 内部写 `final bloc = TaskBloc()` 或创建 Controller，会导致每次组件重绘都重复创建实例丢失状态；必须交由 `BlocProvider` / `StatefulWidget.initState` 托管。

5. ❌ **严禁硬编码文案与色彩**：
   - 文本必须走国际化资源 `AppLocalizations.of(context)`；颜色必须走 `Theme.of(context).colorScheme`。

6. ❌ **严禁忽略 `const` 构造函数**：
   - 所有不需要响应外部状态变动的组件树节点必须显式加上 `const`，使 Flutter 引擎在 Diff 时直接跳过子树对比。

---

## 三、Dart 3 现代语言特性与模式匹配规范

### 1. 模式匹配与密封类 (Pattern Matching & Sealed Classes)
Dart 3 引入的原生 `sealed class` 是实现 UI State 和 Event 的标准：
```dart
sealed class TaskState {}

final class TaskInitial extends TaskState {}
final class TaskLoading extends TaskState {}
final class TaskEmpty extends TaskState {}
final class TaskSuccess extends TaskState {
  final List<Task> tasks;
  const TaskSuccess(this.tasks);
}
final class TaskFailure extends TaskState {
  final String message;
  const TaskFailure(this.message);
}

// 消费端支持编译期穷举检查 (Exhaustiveness checking)
Widget buildView(BuildContext context, TaskState state) {
  return switch (state) {
    TaskInitial() || TaskLoading() => const Center(child: CircularProgressIndicator()),
    TaskEmpty() => const Center(child: Text('No Tasks Found')),
    TaskSuccess(:final tasks) => TaskListView(tasks: tasks),
    TaskFailure(:final message) => ErrorBanner(message: message),
  };
}
```

---

## 四、Flutter 性能与架构守则

### 1. 精确颗粒度的状态重建 (Rebuild Optimization)
避免在整个页面根节点使用大范围 `BlocBuilder`。仅在需要变动的叶子节点处监听：
```dart
// ✅ 推荐：仅局部重建购物车角标文本
Widget buildCartBadge(BuildContext context) {
  return BlocSelector<CartBloc, CartState, int>(
    selector: (state) => state.totalItems,
    builder: (context, count) => Badge(label: Text('$count')),
  );
}
```

### 2. 长列表性能优化
- 必须使用 `ListView.builder` 或 `CustomScrollView` + `SliverList`，严禁在包含未知长度数据时使用 `ListView(children: ...)`（会导致未在屏幕视口内的所有元素全部在内存中初始化完成）。
- 为复杂的列表项指定 `itemExtent` 或 `prototypeItem`，降低布局测量损耗。
