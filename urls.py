from django.conf.urls import url

from Log.views import solveError, testErrorLog

urlpatterns = [
    url(r'^testErrorLog/$', testErrorLog.as_view(), name='测试ErrorLog'),  # 测试ErrorLog

    url(r'^solveError/(.+)/$', solveError.as_view(), name='解决错误通道'),  # 解决错误通道
]


