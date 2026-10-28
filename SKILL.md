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
- **Android Guidelines**: Follow [Android Compose Best Practices](./references/android-guidelines.md).
  - Use `rememberSaveable`, `StateFlow`, `collectAsStateWithLifecycle()`, and `@Stable`/`@Immutable`.
  - Decouple business logic into `ViewModel` or `UseCase`; never expose mutable state directly.
- **Flutter Guidelines**: Follow [Flutter Development Best Practices](./references/flutter-guidelines.md).
  - Use `const` constructors everywhere applicable.
  - Implement separation of UI and business logic via `BlocBuilder`/`BlocListener` or `ConsumerWidget`.
- **Pre-built Templates**:
  - Android MVVM Compose: [templates/android/mvvm_compose](./templates/android/mvvm_compose)
  - Android Clean MVI: [templates/android/clean_mvi](./templates/android/clean_mvi)
  - Flutter BLoC Feature: [templates/flutter/bloc_feature](./templates/flutter/bloc_feature)
  - Flutter Riverpod Clean: [templates/flutter/riverpod_clean](./templates/flutter/riverpod_clean)

---

### Stage 4: Reflection & Verification (质量检查、安全审计与测试)

1. **Run Static Checks & Security Audit**:
   Execute the built-in audit script:
   ```bash
   python scripts/code_quality_check.py <target_directory_or_file>
   ```
   Audits for:
   - **CWE-798**: Hardcoded API keys, JWT tokens, private keys.
   - **Insecure Storage**: Plaintext SharedPreferences instead of EncryptedSharedPreferences / FlutterSecureStorage.
   - **Network Security**: Cleartext HTTP endpoints.
   - **State Leaks**: Coroutines launched without proper lifecycle scope, missing cancellation.
   - **Null Safety & Exceptions**: Raw empty catch blocks, unvalidated nullable casts.
2. **Generate Test Suite**:
   - Unit tests for ViewModels, BLoCs, and UseCases using mock frameworks (MockK / mocktail).
   - Widget & UI tests (Compose `createComposeRule()`, Flutter `testWidgets()`).

---

## 🛠️ Helper Scripts Reference

The skill includes automated Python utilities located in `./scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| [`inspect_codebase.py`](./scripts/inspect_codebase.py) | Scans Android/Flutter projects and prints tech stack, packages, architecture | `python scripts/inspect_codebase.py [path]` |
| [`code_quality_check.py`](./scripts/code_quality_check.py) | Audits Kotlin/Dart code for security vulnerabilities and code smells | `python scripts/code_quality_check.py [path]` |
| [`scaffold_module.py`](./scripts/scaffold_module.py) | Scaffolds standard feature module boilerplate for Android or Flutter | `python scripts/scaffold_module.py --platform <android\|flutter> --name <FeatureName> --arch <mvvm\|mvi\|bloc>` |

---

## 📚 Reference Documentation

- [AI Agent Ontology (本体论模型)](./references/ontology.md): Perception, Cognition, Action, and Memory definitions.
- [Mobile Architecture Selection Guide](./references/architecture-selection.md): Detailed comparison of MVVM, MVI, MVP, Clean, and Feature-First.
- [Android Modern Development Guidelines](./references/android-guidelines.md): Compose, Coroutines, Flow, Hilt, Room.
- [Flutter Modern Development Guidelines](./references/flutter-guidelines.md): Dart 3, BLoC, Riverpod, Dio, Secure Storage.
- [Security & Quality Standards](./references/security-and-quality.md): Mobile OWASP, CWE mapping, and quality gates.
