package com.example.core.network

import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route
import javax.inject.Inject
import javax.inject.Singleton

interface TokenManager {
    fun getAccessToken(): String?
    fun getRefreshToken(): String?
    fun refreshAccessToken(refreshToken: String): String?
    fun clearTokens()
}

/**
 * 线程安全并发 Token 401 自动无感重试 Authenticator
 */
@Singleton
class TokenAuthenticator @Inject constructor(
    private val tokenManager: TokenManager
) : Authenticator {

    private val lock = Any()

    override fun authenticate(route: Route?, response: Response): Request? {
        val currentToken = tokenManager.getAccessToken()

        // 已经重试过 3 次则放弃，防止死循环
        if (responseCount(response) >= 3) {
            return null
        }

        // 双重检查锁：解决并发请求同时 401 的竞态问题
        synchronized(lock) {
            val updatedToken = tokenManager.getAccessToken()

            // 如果其他并发线程已经成功刷新了 Token，直接使用新 Token 重试
            if (updatedToken != null && updatedToken != currentToken) {
                return response.request.newBuilder()
                    .header("Authorization", "Bearer $updatedToken")
                    .build()
            }

            // 否则执行刷新
            val refreshToken = tokenManager.getRefreshToken() ?: return null
            val newAccessToken = tokenManager.refreshAccessToken(refreshToken)

            return if (newAccessToken != null) {
                response.request.newBuilder()
                    .header("Authorization", "Bearer $newAccessToken")
                    .build()
            } else {
                tokenManager.clearTokens()
                null
            }
        }
    }

    private fun responseCount(response: Response): Int {
        var count = 1
        var prior = response.priorResponse
        while (prior != null) {
            count++
            prior = prior.priorResponse
        }
        return count
    }
}
