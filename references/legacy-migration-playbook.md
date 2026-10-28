# Legacy Mobile Modernization & Migration Playbook (老项目改造与渐进式迁移实战手册)

在实际企业级移动端开发中，绝大多数任务并非从零新建工程，而是在现有的历史工程（Legacy Codebase）上进行**渐进式重构**与**技术栈现代化升级**。

---

## 一、Android: XML 视图到 Jetpack Compose 渐进迁移

### 1. 在老旧 Fragment / Activity 中嵌入 Compose (`ComposeView`)
严禁在老项目中搞“休克式全量重写”。推荐按模块或页面局部使用 `ComposeView` 迁移：

```kotlin
class LegacyTaskFragment : Fragment(R.layout.fragment_legacy_task) {

    private var _binding: FragmentLegacyTaskBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _binding = FragmentLegacyTaskBinding.inflate(inflater, container, false)
        
        // ⚠️ 致命避坑：必须设置生命周期销毁策略！
        // 默认情况下 ComposeView 在 DetachFromWindow 时就会被销毁，导致 Fragment 转入后台返回时界面白屏或内存泄漏。
        binding.composeContainer.apply {
            setViewCompositionStrategy(
                ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed
            )
            setContent {
                MaterialTheme {
                    TaskListRoute(onNavigateToDetail = { id -> navigateToDetail(id) })
                }
            }
        }
        return binding.root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

### 2. 在 Compose 中嵌入遗留原生控件 (`AndroidView`)
对于地图（MapView）、广告 SDK、自定义 SurfaceView 或图表库等暂无纯 Compose 实现的组件，使用 `AndroidView` 桥接：
```kotlin
@Composable
fun LegacyMapViewWrapper(modifier: Modifier = Modifier) {
    AndroidView(
        factory = { context ->
            com.google.android.gms.maps.MapView(context).apply {
                onCreate(null)
            }
        },
        update = { view ->
            view.onResume()
        },
        modifier = modifier
    )
}
```

---

## 二、Flutter: 从 GetX / 老旧 Provider 迁移至 BLoC / Riverpod

### 1. 为什么大厂必须将 GetX 迁移为 BLoC / Riverpod？
* **GetX 的工程隐患**：全全局单例 (`Get.put`) 隐藏了依赖树，导致内存生命周期不受控、状态跨页面污染、以及极其难以编写确定性的单元测试（无法 Mock 全局单例）。
* **BLoC / Riverpod 的优势**：编译期类型安全、显式的不可变状态转移、严格的作用域生命周期控制以及原生支持声明式测试。

### 2. 三步渐进式迁移法
1. **第一步：解耦数据与实体模型**
   - 将原先在 `GetxController` 中混杂的变量提取为纯粹的不可变数据类（Immutable State）。
2. **第二步：定义事件驱动管道 (UDF)**
   - 将 Controller 中的直接方法调用（如 `controller.updateName()`）转换为显式的 Event（如 `NameChangedEvent`），引入 `TaskBloc`。
3. **第三步：替换 UI 渲染节点**
   - 将所有 `Obx(() => ...)` 逐一替换为 `BlocBuilder<TaskBloc, TaskState>`，路由由 `Get.to()` 替换为 `GoRouter`。

---

## 三、Java 到 Kotlin 协程迁移避坑

1. **Callback 地狱转挂起函数**：
   - 使用 `suspendCancellableCoroutine` 将基于 Listener / Callback 的 Java 接口包装为挂起函数，并务必处理 `continuation.invokeOnCancellation { ... }` 避免协程取消后底层连接泄漏。
2. **空安全隐患（Platform Types）**：
   - 引用旧 Java 代码返回的变量（带感叹号 `String!`）时，严禁直接当做非空使用，必须立即显式赋予可空声明 `String?` 并做空校验。
