# Mobile Security & Quality Standards (移动端安全与代码质量标准)

## 一、移动安全审计准则 (基于 OWASP Mobile Top 10 & CWE)

| 漏洞类型 | CWE 编号 | 风险场景与典型缺陷 | 防御策略与合规代码 |
|---|---|---|---|
| **硬编码凭证** | **CWE-798** | 在源码或配置常量中硬编码 API Key、JWT Token、私钥或密码 | 严禁源码存密钥。必须通过 `local.properties`、BuildConfig、CI/CD 环境变量注入，或使用 Native NDK 加密串 |
| **明文存储敏感数据** | **CWE-312** | 将 Token、密码明文写入 Android `SharedPreferences` 或 Flutter `SharedPreferences` | Android 使用 `EncryptedSharedPreferences` / Jetpack Security；Flutter 使用 `flutter_secure_storage` (KeyStore / Keychain) |
| **明文网络通信** | **CWE-319** | 使用 `http://` 传输数据，未配置网络安全配置 (Network Security Config) | 强制使用 HTTPS，Android `network_security_config.xml` 中禁用 `cleartextTrafficPermitted="true"` |
| **SQL 注入** | **CWE-89** | 在 SQLite / Room 中使用字符串拼接构建 SQL 查询 | 强制使用参数化查询（如 Room `@Query("SELECT * FROM task WHERE id = :id")`） |
| **组件暴露与隐式 Intent** | **CWE-926** | `AndroidManifest.xml` 中 Activity/Service 未设置 `android:exported="false"` | 非外部唤起组件一律显式设置 `android:exported="false"`；必须导出的组件增加自定义权限保护 |
| **敏感日志泄露** | **CWE-532** | 生产环境使用 `Log.d()` / `print()` 输出用户手机号、Token、身份证号 | 生产环境通过 Proguard/R8 剥离日志，或统一采用 Timber / 自定义 Logger 针对 Release 禁用输出 |

---

## 二、代码质量检查清单 (Quality Gates)

### 1. Android / Kotlin 检查项
- [ ] 命名规范：类名为 `PascalCase`，函数与变量为 `camelCase`，常量为 `UPPER_SNAKE_CASE`。
- [ ] 协程作用域：严禁使用 `GlobalScope.launch`，必须绑定 `viewModelScope` 或 `lifecycleScope`。
- [ ] 异常安全：网络与 IO 调用必须包含优雅降级或 `runCatching` / `Result` 封装，禁止吞掉异常（空 catch 块）。
- [ ] Compose 重组：列表项必须声明 `key` 参数（如 `items(tasks, key = { it.id })`）。

### 2. Flutter / Dart 检查项
- [ ] 命名规范：文件名与库名为 `snake_case.dart`，类名为 `UpperCamelCase`，方法为 `lowerCamelCase`。
- [ ] 空安全（Null Safety）：禁止随意使用非空断言操作符 `!`，优先使用 `?.`、`??` 或条件模式匹配。
- [ ] 资源释放：检查所有 Controllers, StreamSubscriptions 是否在 `dispose()` 中关闭。
- [ ] 性能优化：检查循环中是否未加 const，长列表是否使用了 `ListView.builder` 而非 `ListView(children: ...)`。
