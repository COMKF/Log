import logging
import traceback
import datetime

import requests
from django.http import JsonResponse

from Log.models import Error_msg

EMAIL_URL = 'http://118.89.222.238/email/send_emil/'

TO_EMAILS = ['1943336161@qq.com', 'mjguocn@163.com']

def log_exception(function):
    '''
    记录函数发生错误时的堆栈信息，方便跟踪与查错。

    :param function:
    :return:
    '''

    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            request = args[0]
            scheme = request.scheme
            path = request.path
            method = request.method
            data = request.body
            host = request.get_host()
            if data == b'':
                data = '{}'
            else:
                # data = str(data, encoding='utf-8')
                pass
            try:
                # 生成500错误记录
                build_500_http_error(method, path, scheme)
            except:
                send_error_info_to_email('生成500错误记录爆炸了' + path)

            try:
                # 生成错误的堆栈信息
                build_traceback_error(data, scheme, path, method)
            except:
                send_error_info_to_email('生成堆栈信息爆炸了' + path)

            try:
                # 向邮箱发送警报信息
                update_error_msg_AND_send_by_time(scheme, path, method, host)
            except:
                pass

            # 在这里可自定义返回的数据
            return JsonResponse({'ok': False, 'msg': '服务器提了一个问题，程序员正在解答。'})  # 默认返回{'ok': False}
        finally:
            pass

    return wrap


def build_500_http_error(method, path, scheme):
    '''
    生成500错误记录。

    :param method:
    :param path:
    :param scheme:
    :return:
    '''
    log = logging.getLogger('error_server_log')  # 加载记录器
    msg = '"' + str(method) + ' ' + str(path) + ' ' + str(scheme).upper() + '/1.1"' + ' 500'
    log.error(msg)


def build_traceback_error(data, scheme, path, method):
    '''
    生成错误的堆栈信息。

    :param data:
    :param scheme:
    :param path:
    :param method:
    :return:
    '''
    log = logging.getLogger('exception_log')  # 加载记录器
    msg = 'scheme:' + str(scheme) + ' path:' + str(path) + ' method:' + str(method) + ' data:' + str(data)
    # log 堆栈信息时，堆栈信息中不能有中文（或者说必须全部是英文），因为源代码里，是用ascii进行解析的。
    log.exception(msg)


def update_error_msg_AND_send_by_time(scheme, path, method, host):
    '''
    根据错误的情况的逻辑处理。

    :param scheme:
    :param path:
    :param method:
    :return:
    '''
    msg = ''
    msg += '请求方式：' + scheme + '\r\n'
    msg += 'url：' + path + '\r\n'
    msg += '方法：' + method + '\r\n'

    traceback_info = traceback.format_exc()

    error_msgs = Error_msg.objects.filter(path=path, state='1')
    if error_msgs:
        error_msg = error_msgs.first()
        error_msg.count += 1
        # if error_msg.last_send_time + datetime.timedelta(hours=3) > datetime.datetime.now() + datetime.timedelta(
        #         hours=4):
        if error_msg.last_send_time + datetime.timedelta(hours=3) > datetime.datetime.now():
            # 三小时之内不重复发送
            pass
        else:
            # 三小时之后再次发送，并更新最后一次发送的时间
            error_msg.last_send_time = datetime.datetime.now()
            msg += '错误发生时间：%s' % error_msg.creat_time.strftime("%Y-%m-%d %H:%M:%S") + '\r\n'
            msg += '已发生错误：%s次' % str(error_msg.count) + '\r\n'
            msg += '堆栈信息：\r\n' + traceback_info + '\r\n'
            msg += '请尽快处理！！\r\n若已解决，请点击http://' + host + '/solveError/' + path + '\r\n'
            msg += '请注意，该url没有确认的步骤，会改变该错误的状态，请务必真正解决后再点击，不能随意点击。\r\n'
            send_error_info_to_email(msg)
        error_msg.save()
    else:
        Error_msg(path=path, last_send_time=datetime.datetime.now()).save()
        msg += '错误发生时间：%s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\r\n'
        msg += '已发生错误：1次' + '\r\n'
        msg += '堆栈信息：\r\n' + traceback_info + '\r\n'
        msg += '请尽快处理！！\r\n若已解决，请点击http://' + host + '/solveError/' + path + '\r\n'
        msg += '请注意，该url没有确认的步骤，会改变该错误的状态，请务必真正解决后再点击，不能随意点击。\r\n'
        send_error_info_to_email(msg)


def send_error_info_to_email(msg, title='服务错误警报！！（来自：alipay_zzjj项目）'):
    '''
    向邮箱发送警报信息。

    :param msg:
    :return:
    '''
    # 正常的处理办法
    # send_mail('服务错误警报！！（来自：alipay_zzjj项目）', msg, settings.EMAIL_HOST_USER, TO_EMAILS, fail_silently=False)

    # 委屈求全的处理办法
    data = {'title': title, 'msg': msg, 'TO_EMAILS': TO_EMAILS}
    re = requests.post(url=EMAIL_URL, json=data)
    if re.content != b'success':
        error_msgs = Error_msg.objects.filter(path='send_email_error')
        if error_msgs:
            error_msg = error_msgs.first()
            error_msg.last_send_time = datetime.datetime.now()
            error_msg.save()
        else:
            Error_msg(path='send_email_error', last_send_time=datetime.datetime.now()).save()
