import json

import datetime

from django.http import JsonResponse

from Log.models import UserOperateRecord
from main.models import OpenUser


def log_user_operate(function):
    '''
    记录用户的行为。

    :param function:
    :return:
    '''

    def wrap(*args, **kwargs):
        request = args[0]  # 获取request
        path = request.path  # url
        method = request.method  # request的方法
        host = request.get_host()  # 请求地址

        try:
            data = json.loads(request.body)
        except:
            if method == 'GET':
                data = request.GET  # 请求的数据
            elif method == 'POST':
                data = request.POST  # 请求的数据
            else:
                raise Exception('wrong request method')

        param_method = data.get('method', 'Undefined')

        if request.user.is_authenticated():
            user = OpenUser.objects.get(user=request.user)
        else:
            user = OpenUser.objects.get(alipay_user_id='NoUser')

        # uor, new_flag = UserOperateRecord.objects.get_or_create(user=user, path=path,
        #                                                         creat_time_by_day=datetime.datetime.now(),
        #                                                         incident=param_method)
        uor_filter = UserOperateRecord.objects.filter(user=user, path=path,
                                                      creat_time_by_day=datetime.datetime.now(),
                                                      incident=param_method)
        if uor_filter:
            uor = uor_filter.first()
            new_flag = False
        else:
            uor = UserOperateRecord.objects.create(user=user, path=path,
                                                   creat_time_by_day=datetime.datetime.now(),
                                                   incident=param_method)
            new_flag = True

        if not new_flag:
            uor.count = uor.count + 1

        uor.Field1 = method
        uor.Field2 = host

        if uor.Field3 != '有错误':
            if not new_flag:
                uor.request_data += '----'
            if isinstance(data, bytes):
                uor.request_data += data.decode('utf-8')
            elif isinstance(data, str):
                uor.request_data += data
            elif isinstance(data, dict):
                uor.request_data += str(data)

        try:
            start_time = datetime.datetime.now()
            re = function(*args, **kwargs)
            end_time = datetime.datetime.now()

            run_time = (end_time - start_time).total_seconds()  # 运行时间

            if new_flag:
                uor.run_time = str(run_time)
                if isinstance(re, JsonResponse):
                    uor.response_data = str(json.loads(re.content))
                else:
                    uor.response_data = (re.content).decode('utf-8')  # 返回的数据
            else:
                uor.run_time += '----' + str(run_time)
                if isinstance(re, JsonResponse):
                    uor.response_data += '----' + str(json.loads(re.content))
                else:
                    uor.response_data += '----' + (re.content).decode('utf-8')  # 返回的数据

            uor.save()
            return re
        except Exception as e:
            uor.Field3 = '有错误'
            uor.save()
            raise

    return wrap
