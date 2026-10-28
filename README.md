# Android & Flutter Development Agent Skill

> 本 Skill 将原 `ai-agent--android-flutter` 项目从外部 Python 脚本演进为原生的 Agent 技能包。深度集成了移动端架构决策、现代技术栈规范（Jetpack Compose / Dart 3 / BLoC / Riverpod）、**Vibe Coding 防御原则与 Negative Constraints（严格禁止项）**、代码质量与 CWE 安全扫描规则、**全层次自动化测试套件（单元测试、Compose/Widget UI 测试、Maestro E2E）**，以及可自动化执行的检测与脚手架工具。

---

## 📁 目录结构

```
android-flutter-agent-skill/
├── SKILL.md                          # Skill 核心入口与工作流定义 (含 YAML Frontmatter 与防御守则)
├── README.md                         # 技能说明文档
├── references/                       # 架构与领域知识库
│   ├── ontology.md                   # 移动端 Agent 本体论模型 (感知、认知、行动、反思)
│   ├── architecture-selection.md     # 架构选型决策矩阵 (MVVM / MVI / Clean / Feature-First)
│   ├── testing-guidelines.md         # 自动化测试金字塔指南 (Unit, UI, Maestro E2E)
│   ├── android-guidelines.md         # Kotlin 2.0+ / Compose 性能、生命周期与禁止项守则
│   ├── flutter-guidelines.md         # Flutter 3.x / Dart 3 模式匹配与状态管理规范
│   └── security-and-quality.md       # OWASP Mobile & CWE 安全合规审计标准
├── templates/                        # 生产级代码模版
│   ├── android/
│   │   ├── mvvm_compose/             # Compose (四态+Modifier) + ViewModel + StateFlow
│   │   └── clean_mvi/                # UDF 单向数据流 Contract
│   ├── flutter/
│   │   ├── bloc_feature/             # BLoC 8.x + Event + State + UI
│   │   └── riverpod_clean/           # Riverpod 2.x AsyncNotifier
│   └── tests/                        # 自动化测试样板
│       ├── android/                  # TaskViewModelTest (Turbine/MockK), TaskListScreenTest (ComposeRule)
│       ├── flutter/                  # task_bloc_test (bloc_test), task_page_test (testWidgets)
│       └── e2e/                      # maestro_flow.yaml (跨端声明式回归脚本)
└── scripts/                          # 辅助执行脚本
    ├── inspect_codebase.py           # 扫描识别工程类型、依赖库与架构
    ├── code_quality_check.py         # 质量与安全扫描 (CWE漏洞 + 空catch + 非生命周期Flow等)
    ├── scaffold_module.py            # 快速脚手架生成规范化功能模块
    └── generate_tests.py             # 一键生成对应模块的 Unit、UI 和 E2E 自动化测试
```

---

## 🛡️ Agent 行为准则与严格禁止项 (Negative Constraints)

为防止大模型在移动端代码生成中的“过度重构、破坏性修改、私自引库”等通病，本 Skill 深度内置了以下准则：

1. **先规划，后编码**：修改跨 2 个文件以上或变更数据流时，先列出 3-4 行核心步骤说明；未经明确指令，严禁跨包大范围重构。
2. **极简手术式修改**：仅修改目标上下文，严禁随意格式化未修改行或篡改既有命名与业务注释。
3. **单一可信数据源 (UDF)**：UI 状态严格由 ViewModel/BLoC 驱动，对外仅暴露不可变只读状态流。
4. **严格禁止项**：
   * ❌ 严禁私自引入未经批准的第三方依赖（不得随意修改 `build.gradle.kts` / `pubspec.yaml`）。
   * ❌ 严禁在 UI 作用域内随意开启裸协程（严禁使用 `GlobalScope`）。
   * ❌ 严禁使用普通 `collectAsState()` 收集 Flow（必须使用 `collectAsStateWithLifecycle()`）。
   * ❌ 严禁静默吃掉异常（禁止空 catch 块）。
   * ❌ 严禁硬编码资源（文案走 `stringResource()`，颜色走主题或 `colorResource()`）。
5. **Compose 工业级标准**：
   * 所有公开 Composable 函数第一个可选参数必须为 `modifier: Modifier = Modifier` 并在根布局节点消费。
   * 异步与列表页面必须完整覆盖 `Loading`、`Success`、`Empty`（无数据）、`Error` 四态。

---

## 🧪 自动化测试模块详解

本 Skill 完整贯彻**测试金字塔**设计理念：

### 1. 单元测试 (Unit Testing - 70% 覆盖)
* **Android**：采用 JUnit 5 + MockK + Coroutines Test (`StandardTestDispatcher`) + Turbine，精确拦截和断言 StateFlow 的发射序列。
* **Flutter**：采用 `bloc_test` + `mocktail`，测试 State 状态转换与 Event 响应。

### 2. 界面与组件测试 (UI / Widget Testing - 20% 覆盖)
* **Android**：采用 `createComposeRule()` 进行隔离式 Composable 节点语义查找（`onNodeWithText`, `hasProgressBarRangeInfo`），验证加载与列表渲染。
* **Flutter**：采用 `testWidgets` 与 `WidgetTester.pumpAndSettle()` 进行组件渲染与点击交互验证。

### 3. 端到端自动化回归 (E2E Testing - 10% 覆盖)
* 统一采用现代跨端声明式框架 **Maestro**，通过简洁的 YAML 文件模拟真实用户的点击、输入、列表滚动及截图断言，天然支持 Android 原生与 Flutter。

---

## 🚀 脚本使用指南

### 1. 自动化测试代码生成 (`generate_tests.py`)
为指定功能模块一键生成配套测试：
```bash
# 生成 Android 单元测试、Compose UI 测试及 Maestro E2E
python scripts/generate_tests.py --platform android --name TaskList --package com.example.app --type all

# 生成 Flutter BLoC 测试与 Widget UI 测试
python scripts/generate_tests.py --platform flutter --name TaskList --type all
```

### 2. 代码质量与安全合规扫描 (`code_quality_check.py`)
检查硬编码凭据 (CWE-798)、明文存储 (CWE-312)、明文 HTTP (CWE-319)、非生命周期 Flow 收集、硬编码色值与空 catch：
```bash
python scripts/code_quality_check.py <源码目录或文件>
```

### 3. 扫描与感知工程 (`inspect_codebase.py`)
自动识别项目是否为 Android / Flutter，提取包名、Gradle/pubspec 依赖与当前架构：
```bash
python scripts/inspect_codebase.py <工程根目录路径>
```

### 4. 一键生成标准化功能模块 (`scaffold_module.py`)
```bash
python scripts/scaffold_module.py --platform android --name TaskList --package com.example.myapp
python scripts/scaffold_module.py --platform flutter --name TaskList
```
