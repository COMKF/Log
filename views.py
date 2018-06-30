import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from Log.models import Error_msg, BombboxInfo, CancelBombboxInfoRecord
# from main.models import OpenUser


@method_decorator(ensure_csrf_cookie, name='get')
class testErrorLog(View):
    def get(self, request):
        Error_msg.objects.get(id='123')
        context = {'msg': 'Test is OK.But it should be Error!'}
        return render(request, 'solveError.html', context=context)

    def post(self, request):
        pass

class solveError(View):
    def get(self, request, error_path):
        error_msg = Error_msg.objects.filter(path__contains=error_path, state=1)
        if error_msg:
            error_msg = error_msg.first()
            error_msg.state = 2
            error_msg.solve_time = datetime.datetime.now()
            error_msg.save()
            context = {'msg': 'The Error is fixed now'}
            return render(request, 'solveError.html', context=context)
        else:
            context = {'msg': 'Error Request,Maybe The Error is fixed'}
            return render(request, 'solveError.html', context=context)

    def post(self, request):
        pass

class GetBombboxInfo(View):
    def post(self, request):
        '''
        获取弹框信息

        :param request:
        :param whichview:
        :return:
        '''
        re = {'ok': False}
        info = BombboxInfo.objects.filter(state=True)
        if info:
            Bombbox_info = info.first()
            openuser = OpenUser.objects.get(user=request.user)
            if CancelBombboxInfoRecord.objects.filter(Bombbox=Bombbox_info, user=openuser):
                return JsonResponse(re)
            re['ok'] = True
            re['title'] = Bombbox_info.title
            re['content'] = Bombbox_info.content
            re['Bombbox_info_id'] = Bombbox_info.id
        return JsonResponse(re)


class CancelBombboxInfo(View):
    def post(self, request):
        '''
        取消弹框提示

        :param request:
        :return:
        '''
        data = json.loads(request.body)
        Bombbox_info_id = data.get('Bombbox_info_id', '')
        Bombbox = BombboxInfo.objects.get(id=Bombbox_info_id)
        openuser = OpenUser.objects.get(user=request.user)
        CancelBombboxInfoRecord(Bombbox=Bombbox, user=openuser).save()
        return JsonResponse({})
