# Android & Flutter Development Agent Skill

> 本 Skill 将原 `ai-agent--android-flutter` 项目从外部 Python 脚本演进为原生的 Agent 技能包。深度集成了移动端架构决策、现代技术栈规范（Jetpack Compose / Dart 3 / BLoC / Riverpod）、代码质量与 CWE 安全扫描规则，以及可自动化执行的检测与脚手架工具。

---

## 📁 目录结构

```
android-flutter-agent-skill/
├── SKILL.md                          # Skill 核心入口与工作流定义 (含 YAML Frontmatter)
├── README.md                         # 技能说明文档
├── references/                       # 架构与领域知识库
│   ├── ontology.md                   # 移动端 Agent 本体论模型 (感知、认知、行动、反思)
│   ├── architecture-selection.md     # 架构选型决策矩阵 (MVVM / MVI / Clean / Feature-First)
│   ├── android-guidelines.md         # Kotlin 2.0+ / Compose 性能与生命周期守则
│   ├── flutter-guidelines.md         # Flutter 3.x / Dart 3 模式匹配与状态管理规范
│   └── security-and-quality.md       # OWASP Mobile & CWE 安全合规审计标准
├── templates/                        # 生产级代码模版
│   ├── android/
│   │   ├── mvvm_compose/             # Compose + ViewModel + StateFlow
│   │   └── clean_mvi/                # UDF 单向数据流 Contract
│   └── flutter/
│       ├── bloc_feature/             # BLoC 8.x + Event + State + UI
│       └── riverpod_clean/           # Riverpod 2.x AsyncNotifier
└── scripts/                          # 辅助执行脚本
    ├── inspect_codebase.py           # 扫描识别工程类型、依赖库与架构
    ├── code_quality_check.py         # Kotlin / Dart 代码质量与 CWE 安全扫描
    └── scaffold_module.py            # 快速脚手架生成规范化功能模块
```

---

## 🚀 脚本使用指南

### 1. 扫描与感知工程 (`inspect_codebase.py`)
自动识别项目是否为 Android / Flutter，提取包名、Gradle/pubspec 依赖与当前架构：
```bash
python scripts/inspect_codebase.py <工程根目录路径>
```

### 2. 代码质量与安全合规扫描 (`code_quality_check.py`)
检查硬编码凭据 (CWE-798)、明文存储 (CWE-312)、明文 HTTP (CWE-319)、非空断言与未受控异常：
```bash
python scripts/code_quality_check.py <源码目录或文件>
```

### 3. 一键生成标准化功能模块 (`scaffold_module.py`)
生成符合分层规范的代码模版：
```bash
# 生成 Android Jetpack Compose 模块
python scripts/scaffold_module.py --platform android --name TaskList --package com.example.myapp

# 生成 Flutter BLoC 模块
python scripts/scaffold_module.py --platform flutter --name TaskList
```
