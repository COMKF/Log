import datetime

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from Log.error_Traceback import log_exception
from Log.models import Error_msg

@method_decorator(ensure_csrf_cookie, name='get')
@method_decorator(log_exception, name='get')
@method_decorator(log_exception, name='post')
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
