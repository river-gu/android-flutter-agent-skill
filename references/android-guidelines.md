# Modern Android (Kotlin + Jetpack Compose) Guidelines

## 一、核心技术栈与架构基线 (2025 - 2026)

- **语言与版本**：100% 纯 Kotlin（拒绝 Java 混编），启用严格空安全检查，Kotlin 2.0+ (K2 编译器)。
- **UI 框架**：Jetpack Compose (BOM 最新稳定版), Material 3。
- **架构模式**：Clean Architecture + MVI / MVVM（单向数据流 UDF）。
- **异步与并发**：Kotlin Coroutines + Flow (`StateFlow`, `SharedFlow`)。
- **依赖注入**：Dagger Hilt (推荐) 或 Koin。
- **网络与持久化**：Retrofit / Ktor Client + Kotlinx Serialization, Room Database, DataStore Preferences。
- **架构基础**：AndroidX ViewModel, Navigation Compose。

---

## 二、核心操作守则与严格禁止项 (Negative Constraints)

### 1. 严格禁止项
* ❌ **禁止私自引入第三方依赖**：不得在 `build.gradle.kts` 中添加未经批准的外部库。
* ❌ **禁止在 Compose 作用域内随意开启裸协程**：必须使用 `LaunchedEffect` 或有稳定 Key 的 `rememberCoroutineScope`，严禁无受控作用域调用。
* ❌ **禁止忽略生命周期收集 Flow**：UI 层收集 Flow 时必须使用 `collectAsStateWithLifecycle()`，禁止在后台持续占用资源。
* ❌ **禁止使用 GlobalScope**：所有协程必须受控于 `viewModelScope` 或结构化并发容器。
* ❌ **禁止静默吃掉异常**：不得写出空的 `catch (e: Exception) {}`，必须通过明确的 UI 错误状态或单次事件（Single Event）向上抛出明确错误。
* ❌ **禁止硬编码资源**：界面文案、图标颜色必须走 `stringResource()`、`colorResource()` 或主题 Token，严禁在 UI 中写死字符串与十六进制色值。

---

## 三、Jetpack Compose 关键规范与性能守则

### 1. 状态提升 (State Hoisting) 与双层组件拆分
* **容器型 Composable（Container / Route）**：负责接入 ViewModel、收集 UIState、向 ViewModel 分发事件及处理系统级导航。
* **展示型 Composable（Stateless UI）**：纯函数，仅接收状态数据（Immutable State）与用户操作 Lambda 回调，极易复用与测试。
* **Modifier 首选参数消费**：所有公开的 Composable 函数第一个可选参数必须为 `modifier: Modifier = Modifier`，并在顶层根布局节点消费。

```kotlin
// 1. 容器型 Composable
@Composable
fun TaskListRoute(
    viewModel: TaskViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    TaskListContent(
        uiState = uiState,
        onToggleTask = viewModel::toggleTask,
        onNavigateToDetail = onNavigateToDetail,
        onRetry = viewModel::refresh,
        modifier = modifier
    )
}

// 2. 展示型 Composable (纯无状态)
@Composable
fun TaskListContent(
    uiState: TaskUiState,
    onToggleTask: (String) -> Unit,
    onNavigateToDetail: (String) -> Unit,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(modifier = modifier) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            when (uiState) {
                is TaskUiState.Loading -> CircularProgressIndicator(Modifier.align(Alignment.Center))
                is TaskUiState.Empty -> Text(
                    text = stringResource(R.string.no_tasks_available),
                    modifier = Modifier.align(Alignment.Center)
                )
                is TaskUiState.Success -> LazyColumn {
                    items(uiState.tasks, key = { it.id }) { task ->
                        TaskItem(task = task, onToggleDone = onToggleTask)
                    }
                }
                is TaskUiState.Error -> ErrorView(message = uiState.message, onRetry = onRetry)
            }
        }
    }
}
```

### 2. 四态完备覆盖 (Loading / Success / Empty / Error)
所有列表或异步加载页面，必须显式定义并处理四种基础状态分支，避免空列表无响应或加载失败无交互：
* `Loading`：骨架屏或加载指示器。
* `Success`：正向数据内容渲染。
* `Empty`：无数据时的空态图文指引与引导创建操作。
* `Error`：明确的错误提示信息与重试（Retry）按钮。

### 3. 避免不必要的重组 (Recomposition Optimization)
* **参数稳定性**：对传递给 Composable 的复杂对象使用 `@Immutable` 或 `@Stable` 注解，避免编译器认为参数不稳定导致全量重组。
* **不可变集合**：优先使用 `kotlinx.collections.immutable`（如 `ImmutableList`），避免使用普通 `List` 导致 Compose 误判不稳定。
* **高频计算与 Lambda**：高频创建的对象使用 `remember` 缓存，列表滚动联动派生状态使用 `remember(key) { derivedStateOf { ... } }`。

---

## 四、ViewModel 与状态流规范

### 1. 单向数据流 (UDF) 状态设计示范
```kotlin
// 密封接口清晰表达四态
sealed interface TaskUiState {
    data object Loading : TaskUiState
    data object Empty : TaskUiState
    data class Success(val tasks: List<Task>, val isRefreshing: Boolean = false) : TaskUiState
    data class Error(val message: String) : TaskUiState
}

@HiltViewModel
class TaskViewModel @Inject constructor(
    private val getTasksUseCase: GetTasksUseCase,
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher
) : ViewModel() {

    private val _uiState = MutableStateFlow<TaskUiState>(TaskUiState.Loading)
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    init {
        loadTasks()
    }

    fun loadTasks() {
        viewModelScope.launch(ioDispatcher) {
            _uiState.value = TaskUiState.Loading
            getTasksUseCase()
                .catch { e -> 
                    _uiState.value = TaskUiState.Error(e.localizedMessage ?: "Unknown error") 
                }
                .collect { tasks ->
                    _uiState.value = if (tasks.isEmpty()) {
                        TaskUiState.Empty
                    } else {
                        TaskUiState.Success(tasks)
                    }
                }
        }
    }
}
```

### 2. 调度器注入 (Dispatcher Injection)
严禁硬编码 `Dispatchers.IO` 或 `Dispatchers.Default`，必须通过依赖注入（如 `@IoDispatcher`）注入 `CoroutineDispatcher`，以支持单元测试中无缝替换为 `StandardTestDispatcher`。
