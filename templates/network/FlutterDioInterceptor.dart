import 'package:dio/dio.dart';

abstract class TokenStorage {
  Future<String?> getAccessToken();
  Future<String?> getRefreshToken();
  Future<String?> refreshToken(String refreshToken);
  Future<void> clearTokens();
}

/// 基于 Dio QueuedInterceptor 的并发安全 Token 自动无感刷新拦截器
class TokenInterceptor extends QueuedInterceptor {
  final Dio dio;
  final TokenStorage tokenStorage;

  TokenInterceptor({required this.dio, required this.tokenStorage});

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await tokenStorage.getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      final refreshToken = await tokenStorage.getRefreshToken();
      if (refreshToken == null) {
        await tokenStorage.clearTokens();
        return handler.next(err);
      }

      try {
        // QueuedInterceptor 自动阻塞队列中的后续请求，直到当前刷新完成
        final newAccessToken = await tokenStorage.refreshToken(refreshToken);
        if (newAccessToken != null) {
          final options = err.requestOptions;
          options.headers['Authorization'] = 'Bearer $newAccessToken';

          // 使用新 Token 重试原请求
          final response = await dio.fetch(options);
          return handler.resolve(response);
        } else {
          await tokenStorage.clearTokens();
        }
      } catch (e) {
        await tokenStorage.clearTokens();
      }
    }
    handler.next(err);
  }
}
