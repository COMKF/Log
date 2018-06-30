from django.conf.urls import url

from Log.views import solveError, testErrorLog, GetBombboxInfo, CancelBombboxInfo

urlpatterns = [
    url(r'^testErrorLog/$', testErrorLog.as_view(), name='测试ErrorLog'),  # 测试ErrorLog

    url(r'^solveError/(.+)/$', solveError.as_view(), name='解决错误通道'),  # 解决错误通道

    url(r'^GetBombboxInfo/', GetBombboxInfo.as_view(), name='获取页面提示框'),
    url(r'^CancelBombboxInfo/', CancelBombboxInfo.as_view(), name='取消提示框'),
]


