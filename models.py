from django.db import models


class Error_msg(models.Model):
    '''
    系统错误记录表。
    '''
    path = models.CharField(max_length=50, verbose_name='url路径')
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name='错误的首次生成时间')
    count = models.IntegerField(default=1, verbose_name='错误记录数')
    last_send_time = models.DateTimeField(verbose_name='最后一次向邮箱发送警报的时间')
    state = models.CharField(max_length=2, choices=[('1', "未处理"), ('2', "已处理")], verbose_name='错误处理进度', default='1')
    solve_time = models.DateTimeField(verbose_name='解决时间', null=True, blank=True)

    class Meta:
        verbose_name = "程序错误信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class Url_state(models.Model):
    '''
    url状态记录表。
    '''
    path = models.CharField(max_length=50, verbose_name='url路径')
    break_time = models.DateTimeField(verbose_name='url瘫痪时间', null=True, blank=True)
    state = models.CharField(max_length=2, choices=[('1', "正常"), ('2', "瘫痪中")], verbose_name='url状态', default='1')
    msg = models.CharField(max_length=60, verbose_name='url状态', default='该服务正在维护，暂停使用。请各位用户谅解，对您造成的不便，我们深表歉意。')

    class Meta:
        verbose_name = "程序url状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class UserOperateRecord(models.Model):
    '''
    用户行为记录表

    '''
    # user = models.ForeignKey(OpenUser, verbose_name='支付宝用户') # 需要与当前系统的用户关联起来
    path = models.CharField(max_length=50, verbose_name='url路径')
    incident = models.CharField(max_length=50, verbose_name='事件（自定义）')
    count = models.IntegerField(default=1, verbose_name='记录数')
    creat_time_by_minutes = models.DateTimeField(auto_now_add=True, verbose_name='产生时间(精确到分钟)')
    creat_time_by_day = models.DateField(auto_now_add=True, verbose_name='产生时间(精确到天)')
    request_data = models.TextField(verbose_name='请求数据')
    response_data = models.TextField(verbose_name='返回数据')
    run_time = models.TextField(verbose_name='运行时间（秒）')

    Field1 = models.CharField(max_length=50, verbose_name='保留字段1')
    Field2 = models.CharField(max_length=50, verbose_name='保留字段2')
    Field3 = models.CharField(max_length=50, verbose_name='保留字段3')

    class Meta:
        verbose_name = '用户行为记录'
        verbose_name_plural = verbose_name


class BombboxInfo(models.Model):
    '''
    页面弹框信息
    '''

    title = models.CharField(max_length=20, default='', verbose_name='标题')
    content = models.CharField(max_length=150, default='', verbose_name='内容')
    state = models.BooleanField(default=False, verbose_name='是否启用')

    class Meta:
        verbose_name = "弹框信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class CancelBombboxInfoRecord(models.Model):
    '''
    取消弹框记录
    '''
    Bombbox = models.ForeignKey(BombboxInfo, verbose_name='弹框信息', null=True, blank=True)

    # user = models.ForeignKey(OpenUser, verbose_name='用户', null=True, blank=True) # 需要与当前系统的用户关联起来

    class Meta:
        verbose_name = '取消弹框记录'
        verbose_name_plural = verbose_name
