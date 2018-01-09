from django.http import JsonResponse

from Log.models import Url_state


def check_url_state(function):
    '''
    在调用服务前，先检测该url是否处理可用状态。

    :param function:
    :return:
    '''

    def wrap(*args, **kwargs):
        request = args[0]
        path = request.path
        us = Url_state.objects.filter(path=path, state='2')
        if us:
            return JsonResponse({'ok': False, 'msg': us.first().msg})  # 默认返回{'ok': False}
        else:
            return function(*args, **kwargs)

    return wrap
