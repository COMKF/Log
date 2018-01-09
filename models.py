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
