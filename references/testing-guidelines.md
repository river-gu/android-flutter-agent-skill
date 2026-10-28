# Mobile Automated Testing Guidelines (移动端自动化测试权威指南)

本指南涵盖 **Android (Kotlin / Jetpack Compose)** 与 **Flutter (Dart 3)** 的全层次测试金字塔：单元测试 (Unit Tests)、组件/界面测试 (Widget / Compose Tests) 与 端到端自动化测试 (E2E Tests)。

```
             ┌─────────────────────────┐
             │       E2E 测试          │  Maestro / Integration Test
             │    (用户旅程自动化)     │  占比 ~10%
             ├─────────────────────────┤
             │      UI / 组件测试      │  Compose TestRule / WidgetTester
             │   (组件渲染与交互契约)  │  占比 ~20%
             ├─────────────────────────┤
             │        单元测试         │  JUnit 5 + MockK / bloc_test + mocktail
             │   (业务逻辑、State、VM) │  占比 ~70%
             └─────────────────────────┘
```

---

## 一、Android 自动化测试体系

### 1. 单元测试 (ViewModel, UseCase, Repository)
* **核心依赖**：
  * `junit:junit:4.13.2` 或 `org.junit.jupiter:junit-jupiter`
  * `io.mockk:mockk:1.13.10` (Kotlin 首选 Mock 库)
  * `org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0` (`StandardTestDispatcher`)
  * `app.cash.turbine:turbine:1.1.0` (专用于 StateFlow / SharedFlow 异步断言)

* **ViewModel 测试规范**：
  * 必须使用 `StandardTestDispatcher` 或 `UnconfinedTestDispatcher` 替换主线程调度器 (`Dispatchers.setMain`)。
  * 使用 Turbine 严格按序断言 StateFlow 的发射值：
  ```kotlin
  @Test
  fun `loadTasks emits Loading then Success`() = runTest {
      coEvery { repository.getTasks() } returns flowOf(listOf(Task("1", "Test", false)))

      viewModel.uiState.test {
          assertEquals(TaskUiState.Loading, awaitItem())
          val successState = awaitItem() as TaskUiState.Success
          assertEquals(1, successState.tasks.size)
          cancelAndIgnoreRemainingEvents()
      }
  }
  ```

### 2. Jetpack Compose UI 测试
* **核心依赖**：`androidx.compose.ui:ui-test-junit4`, `androidx.compose.ui:ui-test-manifest`
* **规范**：
  * 使用 `createComposeRule()` 启动隔离渲染环境，无需启动完整 Activity。
  * 通过语义树节点 (Semantics Node) 查找元素并触发点击、滚动、文本输入：
  ```kotlin
  @get:Rule
  val composeTestRule = createComposeRule()

  @Test
  fun taskItem_showsTitle_andTogglesCheckbox() {
      var isToggled = false
      composeTestRule.setContent {
          TaskItem(
              task = Task("1", "Clean Room", isDone = false),
              onToggleDone = { isToggled = true }
          )
      }

      composeTestRule.onNodeWithText("Clean Room").assertIsDisplayed()
      composeTestRule.onNode(hasRole(Role.Checkbox)).performClick()
      assertTrue(isToggled)
  }
  ```

---

## 二、Flutter 自动化测试体系

### 1. 单元与状态管理测试 (BLoC & Riverpod)
* **核心依赖**：`flutter_test`, `bloc_test: ^9.1.7`, `mocktail: ^1.0.4`
* **BLoC 测试规范**：
  * 使用 `blocTest` 声明式测试事件注入（`act`）与状态序列断言（`expect`）：
  ```dart
  blocTest<TaskBloc, TaskState>(
    'emits [TaskLoading, TaskSuccess] when TaskRequested is added',
    build: () => TaskBloc(),
    act: (bloc) => bloc.add(TaskRequested()),
    expect: () => [
      isA<TaskLoading>(),
      isA<TaskSuccess>().having((s) => s.tasks.length, 'tasks count', 2),
    ],
  );
  ```

### 2. Widget UI 界面测试
* **核心工具**：`testWidgets`, `WidgetTester`, `find`
* **测试规范**：
  * 使用 `tester.pumpWidget()` 挂载被测 Widget。
  * 处理异步事件或动画时调用 `tester.pumpAndSettle()` 确保界面静止。
  * 严禁依赖真实网络，需 Mock 或提供内存级别的假数据：
  ```dart
  testWidgets('TaskPage displays task title and triggers checkbox', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: TaskPage()));
    await tester.pumpAndSettle();

    expect(find.text('Implement BLoC Pattern'), findsOneWidget);
    await tester.tap(find.byType(Checkbox).first);
    await tester.pumpAndSettle();
  });
  ```

---

## 三、跨端 E2E 自动化测试 (Maestro)

### 为什么选择 Maestro？
相比于传统 Appium / Espresso / Flutter Driver，**Maestro** 是目前跨平台（Android & iOS/Flutter）最简洁、容错率最高、声明式的黑盒 E2E 工具：
* 编写简单（简洁的 YAML 文件，无需编译代码）。
* 自带智能等待（自动等待元素加载完成，无 Flaky 测试困扰）。
* 同时支持原生 Android 界面与 Flutter 混合界面。

### 核心测试流 (`maestro_flow.yaml`)
```yaml
appId: com.example.taskmanager
---
- launchApp
- assertVisible: "Task Manager"
- tapOn: "Add Task"
- inputText: "Automated E2E Task"
- tapOn: "Confirm"
- assertVisible: "Automated E2E Task"
- tapOn:
    point: "85%, 20%" # 点击 Checkbox
- takeScreenshot: task_completed
```
