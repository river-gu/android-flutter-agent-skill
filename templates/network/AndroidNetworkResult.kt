package com.example.core.network

import kotlinx.serialization.SerializationException
import retrofit2.Response
import java.io.IOException

sealed interface NetworkResult<out T> {
    data class Success<out T>(val data: T) : NetworkResult<T>
    data class HttpError(val code: Int, val message: String?) : NetworkResult<Nothing>
    data class NetworkError(val exception: IOException) : NetworkResult<Nothing>
    data class ParseError(val exception: SerializationException) : NetworkResult<Nothing>
}

suspend fun <T> safeApiCall(apiCall: suspend () -> Response<T>): NetworkResult<T> {
    return try {
        val response = apiCall()
        val body = response.body()
        if (response.isSuccessful && body != null) {
            NetworkResult.Success(body)
        } else {
            NetworkResult.HttpError(response.code(), response.errorBody()?.string())
        }
    } catch (e: IOException) {
        NetworkResult.NetworkError(e)
    } catch (e: SerializationException) {
        NetworkResult.ParseError(e)
    }
}
