---
name: android-flutter-agent
description: >-
  Expert AI assistant for Android (Kotlin / Jetpack Compose) and Flutter (Dart / BLoC / Riverpod) architecture design,
  code generation, quality assurance, security auditing, and test generation. Use when the user requests building,
  refactoring, inspecting, or migrating Android or Flutter apps across MVVM, MVI, Clean Architecture, and Feature-First patterns.
---

# Android & Flutter Development Agent Skill

This skill transforms the agent into a senior mobile architect and full-cycle development assistant specialized in **Android (Kotlin + Jetpack Compose)** and **Cross-Platform Flutter (Dart 3.x)**. It incorporates the ontology and principles of the `ai-agent--android-flutter` framework, guiding requirements analysis, architecture selection, high-quality code generation, security scanning, and automated testing.

---

## 🛡️ 核心操作守则与防御准则 (Vibe Coding Defense)

为了杜绝大模型在移动端代码生成中的“过度重构、破坏性修改、私自引库”等通病，执行任何任务必须严格遵循以下防御准则：

### 1. 先规划，后编码 (Plan First, Code Later)
- 涉及跨多个组件、数据流调整或修改超过 **2 个文件**时，必须先在回复前列出 **3-4 行核心执行步骤**。
- 未经用户明确确认，**严禁一次性大范围重构**多个包路径下的代码。

### 2. 极简手术式修改 (Surgical Edits Only)
- 仅修改与当前目标功能严格关联的文件与代码行。
- **严禁随意格式化或更改未涉修改项**的变量命名、代码风格或既有业务注解。

### 3. 单一可信数据源 (Single Source of Truth, UDF)
- UI 状态由 ViewModel 或 BLoC 统一管理并驱动，对外仅暴露不可变的只读状态流（如 `StateFlow<UiState>`）。
- UI 组件（Composable / Widget）严禁在内部维护无状态托管的独立业务逻辑。

---

## 🚫 严格禁止项 (Negative Constraints)

在生成和修改代码时，以下行为被绝对禁止：

### 通用与 Android 约束
1. ❌ **严禁私自引入未经批准的第三方依赖**：不得随意修改 `build.gradle.kts` 或 `pubspec.yaml` 添加外部库。
2. ❌ **严禁在 UI 作用域内随意开启裸协程**：Compose 中必须使用 `LaunchedEffect` 或绑定稳定 Key 的 `rememberCoroutineScope`；严禁使用 `GlobalScope`。
3. ❌ **严禁忽略生命周期收集 Flow**：UI 层收集 Flow 时必须使用 `collectAsStateWithLifecycle()`，禁止使用普通 `collectAsState()` 造成后台持续耗能。
4. ❌ **严禁静默吃掉异常**：禁止写出空的 `catch (e: Exception) {}`，必须通过明确的 UI 错误状态或单次事件（Single Event）向上反馈。
5. ❌ **严禁硬编码资源与尺寸**：界面文案走 `stringResource()` / `l10n`，颜色走主题 Token 或 `colorResource()`，严禁写死字符串与十六进制色值；禁止在可自适应布局上死写固定宽度。

### Flutter 专项约束
6. ❌ **严禁跨 `await` 异步缝隙裸用 `BuildContext`**：必须前置校验 `if (!context.mounted) return;` 避免页面退出后调用失效 context 崩溃。
7. ❌ **严禁 Controller / Stream 资源未在 `dispose()` 中注销释放**，杜绝内存泄漏。
8. ❌ **严禁在页面根节点滥用深层 `setState()`**，局部变动必须下沉或采用 `BlocSelector` / `Consumer` 进行精确重建。
9. ❌ **严禁在 `build()` 方法中实例化状态管理对象**（如 `final bloc = TaskBloc()`）。

---

## 🎯 When to Use This Skill

Activate this skill when:
- Creating new Android or Flutter projects, features, screens, or architectural layers.
- Inspecting and diagnosing existing Android or Flutter codebases for anti-patterns, security flaws, or performance bottlenecks.
- Refactoring legacy mobile architectures (e.g., MVC/MVP to MVVM, MVI, or Clean Architecture).
- Selecting state management solutions (BLoC, Riverpod, StateFlow, MVI Reducer) based on project constraints.
- Generating automated unit tests, UI widget/compose tests, and E2E automation test scripts.

---

## 🧭 Four-Stage Agent Workflow (Perception → Cognition → Action → Reflection)

Follow this structured workflow for every mobile development or auditing task:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGENT COGNITIVE WORKFLOW                         │
├─────────────────┬──────────────────┬─────────────────┬─────────────────┤
│  1. PERCEPTION  │   2. COGNITION   │    3. ACTION    │  4. REFLECTION  │
│                 │                  │                 │                 │
│ • Detect Stack  │ • Select Arch    │ • Generate Code │ • Lint / Format │
│ • Parse Spec    │ • Task Breakdown │ • Wire DI & API │ • Security Scan │
│ • Scan Context  │ • Define Models  │ • Write Tests   │ • Best-Practice │
└─────────────────┴──────────────────┴─────────────────┴─────────────────┘
```

### Stage 1: Perception (需求与上下文感知)

1. **Detect Project Environment**:
   - Run the inspection script `python scripts/inspect_codebase.py <project_path>` to identify:
     - Platform: Android (Gradle, Kotlin/Java) or Flutter (`pubspec.yaml`, Dart version).
     - Existing Architecture: MVVM, MVP, Clean, MVI, or unstructured.
     - State Management & DI: Hilt, Koin, Jetpack ViewModel, Flutter BLoC, Riverpod, Provider, GetX.
     - API & Storage: Retrofit, Ktor, Dio, Room, SQLite, Hive, Isar, DataStore.
2. **Extract Requirements**:
   - Core functional points, page specifications, input fields, state transitions, API endpoints, and validation rules.

---

### Stage 2: Cognition (架构推断与任务拆解)

1. **Architecture Decision Matrix**:
   Consult [Architecture Selection Guide](./references/architecture-selection.md) to choose the optimal architecture:
   - **MVVM**: Best for small-to-medium apps, form-driven views, data binding.
   - **MVI (Unidirectional Data Flow)**: Best for complex UI states, gaming/dashboard feeds, undo/redo flows.
   - **Clean Architecture (Domain/Data/Presentation)**: Best for enterprise apps, multi-developer teams, reusable business use cases.
   - **Feature-First**: Recommended for scalable Flutter apps (`features/<feature_name>/domain, data, presentation`).
2. **Domain & State Modeling**:
   - Define immutable State models (e.g., `sealed class` in Kotlin, `freezed` or sealed classes in Dart).
   - Define user Intents/Events and side effects (One-time navigation/toast events).

---

### Stage 3: Action (规范化代码生成与装配)

When generating code, adhere strictly to the platform standards:
- **Android Compose Guidelines**: Follow [Android Compose Best Practices](./references/android-guidelines.md).
  - **Modifier 规范**：所有公开 Composable 函数第一个可选参数必须为 `modifier: Modifier = Modifier`，并在根布局节点消费。
  - **四态完备覆盖**：异步及列表页面必须显式提供 `Loading`、`Success`、`Empty`（无数据）、`Error` 四种状态分支。
  - **状态提升与分层**：严格拆分为容器型 Composable（负责挂载 ViewModel/状态流）与展示型 Composable（纯接收 State 与 Lambda 回调）。
  - **性能与生命周期**：使用 `rememberSaveable`、`collectAsStateWithLifecycle()` 与 `@Stable`/`@Immutable` 避免冗余重组。
- **Flutter Guidelines**: Follow [Flutter Development Best Practices](./references/flutter-guidelines.md).
  - Use `const` constructors everywhere applicable.
  - Implement separation of UI and business logic via `BlocBuilder`/`BlocListener` or `ConsumerWidget`.
- **Pre-built Templates**:
  - Android MVVM Compose: [templates/android/mvvm_compose](./templates/android/mvvm_compose)
  - Android Clean MVI: [templates/android/clean_mvi](./templates/android/clean_mvi)
  - Android Adaptive Layout: [templates/android/adaptive](./templates/android/adaptive)
  - Flutter BLoC Feature: [templates/flutter/bloc_feature](./templates/flutter/bloc_feature)
  - Flutter Riverpod Clean: [templates/flutter/riverpod_clean](./templates/flutter/riverpod_clean)
  - Resilient Network & Auth: [templates/network](./templates/network)
  - Automated Tests: [templates/tests](./templates/tests) (Unit, UI, Maestro E2E)

---

### Stage 4: Reflection & Verification (质量检查、安全审计与自动化测试)

1. **Run Static Checks & Security Audit**:
   Execute the built-in audit script:
   ```bash
   python scripts/code_quality_check.py <target_directory_or_file>
   ```
   Audits for:
   - **CWE-798**: Hardcoded API keys, JWT tokens, private keys.
   - **Insecure Storage**: Plaintext SharedPreferences instead of EncryptedSharedPreferences / FlutterSecureStorage.
   - **Network Security**: Cleartext HTTP endpoints.
   - **Async Gap Safety**: Unsafe `BuildContext` across `await` without `context.mounted`.
   - **State Leaks**: Coroutines launched without proper lifecycle scope, missing cancellation.
   - **Null Safety & Exceptions**: Raw empty catch blocks, unvalidated nullable casts.
2. **Generate Automated Test Suite (Unit + UI + E2E)**:
   Consult [Testing Guidelines](./references/testing-guidelines.md) and execute:
   ```bash
   python scripts/generate_tests.py --platform <android|flutter> --name <FeatureName> --type all --output <test_dir>
   ```
   - **Unit Tests**:
     - Android: MockK + Turbine + Coroutines Test for StateFlow in ViewModels & UseCases.
     - Flutter: `bloc_test` + `mocktail` for BLoC/Cubit event-state verification.
   - **Widget & Compose UI Tests**:
     - Android: Compose `createComposeRule()`, semantics tree verification, state-driven rendering.
     - Flutter: `testWidgets` with `WidgetTester.pumpAndSettle()`.
   - **E2E Integration Flow**:
     - Cross-platform Maestro declarative YAML flows (`maestro_flow.yaml`).

---

## 🛠️ Helper Scripts Reference

The skill includes automated Python utilities located in `./scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| [`inspect_codebase.py`](./scripts/inspect_codebase.py) | Scans Android/Flutter projects and prints tech stack, packages, architecture | `python scripts/inspect_codebase.py [path]` |
| [`code_quality_check.py`](./scripts/code_quality_check.py) | Audits Kotlin/Dart code for security vulnerabilities and code smells | `python scripts/code_quality_check.py [path]` |
| [`scaffold_module.py`](./scripts/scaffold_module.py) | Scaffolds standard feature module boilerplate for Android or Flutter | `python scripts/scaffold_module.py --platform <android\|flutter> --name <FeatureName> --arch <mvvm\|mvi\|bloc>` |
| [`generate_tests.py`](./scripts/generate_tests.py) | Automatically generates Unit Tests, Compose/Widget UI Tests, and Maestro E2E scripts | `python scripts/generate_tests.py --platform <android\|flutter> --name <FeatureName> --type all` |

---

## 📚 Reference Documentation

- [AI Agent Ontology (本体论模型)](./references/ontology.md): Perception, Cognition, Action, and Memory definitions.
- [Mobile Architecture Selection Guide](./references/architecture-selection.md): Detailed comparison of MVVM, MVI, MVP, Clean, and Feature-First.
- [Automated Testing Guidelines (测试金字塔指南)](./references/testing-guidelines.md): Comprehensive guide for Unit, Compose/Widget UI, and Maestro E2E testing.
- [Offline-First & Network Resilience (离线优先与网络弹性)](./references/offline-first-and-network.md): SSOT Database-first Flow, Token 401 Authenticator, NetworkResult sealed hierarchy.
- [Adaptive & Responsive Layouts (折叠屏与大屏适配)](./references/adaptive-layouts.md): WindowWidthSizeClass, List-Detail pattern, LayoutBuilder constraints.
- [Legacy Modernization Playbook (老项目改造与渐进迁移)](./references/legacy-migration-playbook.md): XML to ComposeView lifecycle traps, GetX to BLoC migration, Callback to Coroutine.
- [Android Modern Development Guidelines](./references/android-guidelines.md): Compose, Coroutines, Flow, Hilt, Room.
- [Flutter Modern Development Guidelines](./references/flutter-guidelines.md): Dart 3, BLoC, Riverpod, Dio, Secure Storage.
- [Security & Quality Standards](./references/security-and-quality.md): Mobile OWASP, CWE mapping, and quality gates.
- [Security & Quality Standards](./references/security-and-quality.md): Mobile OWASP, CWE mapping, and quality gates.
