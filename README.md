# Android & Flutter Development Agent Skill

> 本 Skill 将原 `ai-agent--android-flutter` 项目从外部 Python 脚本演进为原生的 Agent 技能包。深度集成了移动端架构决策、现代技术栈规范（Jetpack Compose / Dart 3 / BLoC / Riverpod）、**Vibe Coding 防御原则与双端 Negative Constraints（严格禁止项）**、**离线优先与网络弹性架构**、**折叠屏大屏适配**、**老项目迁移手册**、代码质量与 CWE 安全扫描规则、**全层次自动化测试套件（单元测试、Compose/Widget UI 测试、Maestro E2E）**，以及 **GitHub Actions CI/CD 自动化门禁**。

---

## 📁 目录结构

```
android-flutter-agent-skill/
├── .github/workflows/                 # CI/CD 自动化持续集成门禁
│   └── mobile-quality-gate.yml        # PR 自动触发代码质量与 CWE 安全静态审计
├── SKILL.md                          # Skill 核心入口与工作流定义 (含 YAML Frontmatter 与防御守则)
├── README.md                         # 技能说明文档
├── references/                       # 架构与领域知识库
│   ├── ontology.md                   # 移动端 Agent 本体论模型 (感知、认知、行动、反思)
│   ├── architecture-selection.md     # 架构选型决策矩阵 (MVVM / MVI / Clean / Feature-First)
│   ├── testing-guidelines.md         # 自动化测试金字塔指南 (Unit, UI, Maestro E2E)
│   ├── offline-first-and-network.md  # 离线优先架构、Token 401 并发刷新与 NetworkResult
│   ├── adaptive-layouts.md           # 折叠屏、平板与大屏响应式 (WindowSizeClass / Breakpoints)
│   ├── legacy-migration-playbook.md  # 老工程改造指南 (XML转ComposeView生命周期、GetX迁BLoC)
│   ├── android-guidelines.md         # Kotlin 2.0+ / Compose 性能、生命周期与禁止项守则
│   ├── flutter-guidelines.md         # Flutter 3.x / Dart 3 异步缝隙安全、模式匹配与状态管理规范
│   └── security-and-quality.md       # OWASP Mobile & CWE 安全合规审计标准
├── templates/                        # 生产级代码模版
│   ├── android/
│   │   ├── mvvm_compose/             # Compose (四态+Modifier) + ViewModel + StateFlow
│   │   ├── clean_mvi/                # UDF 单向数据流 Contract
│   │   └── adaptive/                 # 响应式双窗格 List-Detail 布局模版
│   ├── flutter/
│   │   ├── bloc_feature/             # BLoC 8.x + Event + State + UI
│   │   └── riverpod_clean/           # Riverpod 2.x AsyncNotifier
│   ├── network/                      # 企业级网络与鉴权韧性模版
│   │   ├── AndroidNetworkResult.kt   # 统一 NetworkResult<T> 与安全包装函数
│   │   ├── TokenAuthenticator.kt     # 并发安全 Token 401 自动无感刷新 Authenticator
│   │   └── FlutterDioInterceptor.dart# Dio QueuedInterceptor 并发无感换票拦截器
│   └── tests/                        # 自动化测试样板
│       ├── android/                  # TaskViewModelTest (Turbine/MockK), TaskListScreenTest (ComposeRule)
│       ├── flutter/                  # task_bloc_test (bloc_test), task_page_test (testWidgets)
│       └── e2e/                      # maestro_flow.yaml (跨端声明式回归脚本)
└── scripts/                          # 辅助执行脚本
    ├── inspect_codebase.py           # 扫描识别工程类型、依赖库与架构
    ├── code_quality_check.py         # 质量与安全扫描 (CWE漏洞 + 空catch + 非生命周期Flow + 异步context等)
    ├── scaffold_module.py            # 快速脚手架生成规范化功能模块
    └── generate_tests.py             # 一键生成对应模块的 Unit、UI 和 E2E 自动化测试
```

---

## 🛡️ Agent 双端行为准则与严格禁止项 (Negative Constraints)

为防止大模型在移动端代码生成中的“过度重构、破坏性修改、私自引库”等通病，本 Skill 深度内置了以下准则：

1. **先规划，后编码**：修改跨 2 个文件以上或变更数据流时，先列出 3-4 行核心步骤说明；未经明确指令，严禁跨包大范围重构。
2. **极简手术式修改**：仅修改目标上下文，严禁随意格式化未修改行或篡改既有命名与业务注释。
3. **单一可信数据源 (UDF)**：UI 状态严格由 ViewModel/BLoC 驱动，对外仅暴露不可变只读状态流。
4. **Android 核心禁止项**：
   * ❌ 严禁私自引入未经批准的第三方依赖（不得随意修改 `build.gradle.kts`）。
   * ❌ 严禁在 UI 作用域内随意开启裸协程（严禁使用 `GlobalScope`）。
   * ❌ 严禁使用普通 `collectAsState()` 收集 Flow（必须使用 `collectAsStateWithLifecycle()`）。
   * ❌ 严禁硬编码资源与固定尺寸（文案走 `stringResource()`，颜色走主题，避免死写固定宽度导致折叠屏大面积留白）。
   * ❌ 必须遵守 Compose 工业级规范：公开函数首选参数必须为 `modifier: Modifier = Modifier`，页面完整覆盖 `Loading`、`Success`、`Empty`、`Error` 四态。
5. **Flutter 核心禁止项**：
   * ❌ 严禁跨 `await` 异步缝隙裸用 `BuildContext`（必须前置校验 `if (!context.mounted) return;` 避免页面退出后调用失效 context 崩溃）。
   * ❌ 严禁 Controller / Stream 资源未在 `State.dispose()` 中显式销毁。
   * ❌ 严禁在页面根节点滥用深层 `setState()` 造成整树重绘；严禁在 `build()` 内部实例化状态管理对象。
   * ❌ 必须添加 `const` 构造函数；文案走 `AppLocalizations`，颜色走 `Theme.of(context).colorScheme`。

---

## 🚀 脚本使用指南

### 1. 代码质量与安全合规扫描 (`code_quality_check.py`)
检查硬编码凭据 (CWE-798)、明文存储 (CWE-312)、明文 HTTP (CWE-319)、Flutter 异步 Context 裸用、非生命周期 Flow 收集、硬编码色值与空 catch：
```bash
python scripts/code_quality_check.py <源码目录或文件>
```

### 2. 自动化测试代码生成 (`generate_tests.py`)
为指定功能模块一键生成配套测试：
```bash
# 生成 Android 单元测试、Compose UI 测试及 Maestro E2E
python scripts/generate_tests.py --platform android --name TaskList --package com.example.app --type all

# 生成 Flutter BLoC 测试与 Widget UI 测试
python scripts/generate_tests.py --platform flutter --name TaskList --type all
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
