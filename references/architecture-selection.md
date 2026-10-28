# Mobile Architecture Selection Guide (移动端架构选型决策矩阵)

## 一、架构对比总览

| 架构模式 | 核心理念 | 适用场景 | 状态流转 | 测试难易度 | 上手门槛 | 推荐状态库 (Android / Flutter) |
|---|---|---|---|---|---|---|
| **MVVM** | View 绑定 ViewModel，双向/单向数据流动 | 中小型项目、常规 CRUD、表单驱动页面 | ViewModel 暴露 LiveData/StateFlow，View 订阅 | 简单 (VM 纯逻辑) | 低 | Android: ViewModel + StateFlow<br>Flutter: ChangeNotifier / Cubit |
| **MVI** | 单向数据流 (UDF)，用户 Intent 驱动单一 State | 状态复杂页面、高频交互、游戏化/仪表板 | Intent -> Reducer -> Immutable State | 极易 (状态确定性) | 中 | Android: StateFlow + Sealed Class<br>Flutter: Flutter BLoC |
| **Clean Architecture** | 依赖倒置，Domain 层独立于任何 UI 与框架 | 跨端逻辑共享、企业级大型应用、多团队协作 | UI -> UseCase -> Repository -> DataSource | 极易 (全接口解耦) | 高 | Android: Hilt + UseCases<br>Flutter: BLoC / Riverpod + UseCases |
| **Feature-First** | 按业务垂直切片（纵向切分），每个 Feature 自成体系 | 模块化大型应用、微前端/模块化架构 | Feature 内部高内聚，跨 Feature 通过 Router/DI 交互 | 优秀 | 中 | Android: Multi-module Gradle<br>Flutter: `lib/features/<name>/` |

---

## 二、架构决策决策树

```
项目选型决策
│
├── 是全新项目还是老旧项目重构？
│   ├── 老旧项目迁移 (已有 MVP / MVC)
│   │   └── 建议：采用渐进式 MVVM 或 Feature-First 逐模块迁移，避免全量重写
│   │
│   └── 全新项目启动
│       ├── 应用规模评估：
│       │   ├── 小型应用 / MVP 验证原型 (< 5 个页面)
│       │   │   └── 推荐：轻量 MVVM (Android: Compose+ViewModel; Flutter: Riverpod / Cubit)
│       │   │
│       │   ├── 中型应用 (5 - 25 页面，含登录、缓存、多接口调用)
│       │   │   └── 推荐：MVI 或 标准 MVVM (Android: Compose+Hilt+StateFlow; Flutter: BLoC)
│       │   │
│       │   └── 大型 / 企业级应用 (> 25 页面，多团队协同，核心业务复杂)
│       │       └── 推荐：Clean Architecture + Feature-First (垂直切片分包)
```

---

## 三、推荐目录布局规范

### 1. Android Feature-First / Clean 结构
```
com.example.app/
├── core/
│   ├── designsystem/     # Compose 主题、通用组件、字体、图标
│   ├── network/          # Retrofit / OkHttp 配置、拦截器、网络错误包装
│   ├── database/         # Room 数据库定义、通用 TypeConverter
│   └── common/           # 结果封装 Result<T>、扩展函数、调度器注入
├── features/
│   └── user_profile/
│       ├── data/         # RepositoryImpl, RemoteDataSource, LocalDataSource, Entities
│       ├── domain/       # UseCases, RepositoryInterfaces, DomainModels
│       └── presentation/ # Compose Screens, ViewModel, UIState, UIEvent
└── di/                   # 全局 AppModule、Hilt 依赖绑定
```

### 2. Flutter Feature-First / BLoC 结构
```
lib/
├── core/
│   ├── theme/            # ThemeData、色彩、间距常量
│   ├── network/          # Dio 客户端配置、API 拦截器
│   └── error/            # Failure 抽象、Exception 捕获
├── features/
│   └── task_management/
│       ├── data/
│       │   ├── datasources/ # API client, Local DB (Hive / Isar / SQLite)
│       │   ├── models/      # JSON 反序列化 DTOs
│       │   └── repositories/ # TaskRepositoryImpl
│       ├── domain/
│       │   ├── entities/    # 纯业务实体
│       │   ├── repositories/# TaskRepository (抽象接口)
│       │   └── usecases/    # GetTasksUseCase, CreateTaskUseCase
│       └── presentation/
│           ├── bloc/        # TaskBloc, TaskEvent, TaskState
│           ├── pages/       # TaskListPage, TaskDetailPage
│           └── widgets/     # 页面专属子组件
└── main.dart
```
