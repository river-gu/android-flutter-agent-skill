# Offline-First & Network Resilience Guide (离线优先与网络弹性架构)

在现代移动应用开发中，面对弱网、断网与并发请求，必须构建**离线优先（Offline-First）**和**高弹性容错（Network Resilience）**网络层。

---

## 一、单一可信源离线架构 (Single Source of Truth Flow)

### 核心设计原则
* **UI 永远只观察本地数据库**（Room on Android, Isar/Drift on Flutter）。
* **网络请求是后台同步机制**：接口返回的数据直接写入本地数据库，由本地数据库响应式触发 UI 更新。
* **断网无感**：即使处于飞行模式或极端弱网，用户也能即时浏览缓存数据，并在恢复网络后自动增量同步。

```
┌───────────┐         1. 订阅观察 (Flow / Stream)           ┌──────────────┐
│  UI 界面  │ ◄──────────────────────────────────────────── │ 本地数据库   │
└───────────┘                                               │ (Room/Isar)  │
      │                                                     └──────────────┘
      │ 2. 用户操作 (下拉刷新/发帖)                                ▲
      ▼                                                            │ 4. 写入缓存
┌───────────────┐     3. 异步网络调用 (后台调度)     ┌──────────────┴─┐
│  Repository   │ ─────────────────────────────────► │ 远程 REST API  │
└───────────────┘                                    └────────────────┘
```

---

## 二、企业级网络结果密封模型 (`NetworkResult<T>`)

严禁使用普通的 `Result<T>` 配合宽泛的 `Exception`。应使用状态明确的密封类：

```kotlin
sealed interface NetworkResult<out T> {
    data class Success<out T>(val data: T) : NetworkResult<T>
    data class HttpError(val code: Int, val errorBody: String?) : NetworkResult<Nothing>
    data class NetworkError(val throwable: Throwable) : NetworkResult<Nothing>
    data class ParseError(val throwable: Throwable) : NetworkResult<Nothing>
}
```

配套安全包装调用函数：
```kotlin
suspend fun <T> safeApiCall(apiCall: suspend () -> Response<T>): NetworkResult<T> {
    return try {
        val response = apiCall()
        if (response.isSuccessful) {
            val body = response.body()
            if (body != null) NetworkResult.Success(body) 
            else NetworkResult.HttpError(response.code(), "Empty response body")
        } else {
            NetworkResult.HttpError(response.code(), response.errorBody()?.string())
        }
    } catch (e: IOException) {
        NetworkResult.NetworkError(e) // 离线、超时、DNS 失败
    } catch (e: SerializationException) {
        NetworkResult.ParseError(e)   // 字段类型不匹配
    }
}
```

---

## 三、Token 401 自动无感刷新与并发锁 (Authenticator)

### 痛点场景
当用户 Access Token 过期时，页面同时发出了 3 个并发接口（如用户信息、购物车、未读消息数）。如果三个接口同时捕获 401 并发起刷新 Token，会导致并发刷新冲突和凭据失效。

### 解决方案
* **Android (OkHttp Authenticator)**：使用 `synchronized` 互斥块校验当前 Token 是否已被其他并发线程刷新；若已刷新则直接重试，若未刷新则调用刷新接口并重新构建请求。
* **Flutter (Dio QueuedInterceptor)**：使用 `QueuedInterceptor`，利用内部队列自动挂起（Lock）后续并发请求，直到 Token 刷新完成并更新 Header，再批量放行重试。

见模版：
- [Android TokenAuthenticator.kt](../templates/network/TokenAuthenticator.kt)
- [Flutter FlutterDioInterceptor.dart](../templates/network/FlutterDioInterceptor.dart)
