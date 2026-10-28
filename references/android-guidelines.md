# Modern Android (Kotlin + Jetpack Compose) Guidelines

## 一、核心技术栈推荐 (2025 - 2026)

- **语言与版本**：Kotlin 2.0+ (K2 编译器), Java 17/21
- **UI 框架**：Jetpack Compose (BOM 最新稳定版), Material 3
- **异步与并发**：Kotlin Coroutines + Flow (`StateFlow`, `SharedFlow`)
- **依赖注入**：Dagger Hilt (推荐) 或 Koin
- **网络与持久化**：Retrofit 2.x / Ktor Client + Kotlinx Serialization, Room Database, DataStore Preferences
- **架构基础**：AndroidX ViewModel, Navigation Compose

---

## 二、Jetpack Compose 关键规范与性能守则

### 1. 状态提升 (State Hoisting) 与单一数据源
- Composable 函数应尽量保持为无状态（Stateless），将状态（State）与事件（Event）提升到调用方或 ViewModel 中。
```kotlin
// ✅ 推荐：Stateless Composable
@Composable
fun TaskItem(
    task: Task,
    onToggleDone: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier.clickable { onToggleDone(task.id) }) {
        Checkbox(checked = task.isDone, onCheckedChange = { onToggleDone(task.id) })
        Text(text = task.title)
    }
}
```

### 2. 避免不必要的重组 (Recomposition Optimization)
- **参数稳定性**：对传递给 Composable 的复杂对象使用 `@Immutable` 或 `@Stable` 注解，避免编译器认为参数不稳定导致全量重组。
- **避免在 Composable 内部创建对象**：如高频 lambda、Formatter 等，使用 `remember` 缓存。
- **派生状态**：如果计算依赖其他状态，使用 `remember(key) { derivedStateOf { ... } }`。

### 3. 生命周期感知的状态收集
- 在 Compose 中收集 Flow 必须使用 `collectAsStateWithLifecycle()`（引入 `androidx.lifecycle:lifecycle-runtime-compose`），严禁使用普通 `collectAsState()`，以避免后台隐蔽消耗 CPU 与内存。
```kotlin
@Composable
fun TaskScreen(viewModel: TaskViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    // UI rendering
}
```

---

## 三、ViewModel 与并发调度规范

### 1. 单向数据流 (UDF) 状态设计
```kotlin
// 密封接口表示界面状态
sealed interface TaskUiState {
    data object Loading : TaskUiState
    data class Success(val tasks: List<Task>, val isRefreshing: Boolean = false) : TaskUiState
    data class Error(val message: String) : TaskUiState
}

@HiltViewModel
class TaskViewModel @Inject constructor(
    private val getTasksUseCase: GetTasksUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<TaskUiState>(TaskUiState.Loading)
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    init {
        loadTasks()
    }

    fun loadTasks() {
        viewModelScope.launch {
            _uiState.value = TaskUiState.Loading
            getTasksUseCase()
                .catch { e -> _uiState.value = TaskUiState.Error(e.localizedMessage ?: "Unknown error") }
                .collect { tasks -> _uiState.value = TaskUiState.Success(tasks) }
        }
    }
}
```

### 2. 调度器注入 (Dispatcher Injection)
- 严禁硬编码 `Dispatchers.IO` 或 `Dispatchers.Default`，必须通过依赖注入注入 `CoroutineDispatcher`，以支持单元测试中替换为 `TestDispatcher`。
