# 设置主题
import xadmin
from Log.models import *
from xadmin import views


class GlobalSetting(object):  # 全局设置
    site_title = '项目后台数据监控'  # 设置页眉和 HTML 标题。
    site_footer = '聚凡科技公司版权所有，违法必究。'  # 设置页脚
    menu_style = 'accordion'  # 设置左侧侧边栏显示方式。


xadmin.site.register(views.CommAdminView, GlobalSetting)  # 将GlobalSetting中的设置注册到CommAdminView中


class Error_msgAdmin(object):  # 注册BombboxInfoAdmin。注意，它继承的是object

    list_display = ['path', 'creat_time', 'count', 'last_send_time', 'state', 'solve_time']
    list_filter = ['creat_time', 'last_send_time', 'state', 'solve_time']
    list_editable = ['state']  # 设置可以直接在页面上编辑的字段


xadmin.site.register(Error_msg, Error_msgAdmin)  # 将管理器注册、


class Url_stateAdmin(object):  # 注册BombboxInfoAdmin。注意，它继承的是object

    list_display = ['path', 'break_time', 'state', 'msg']
    list_filter = ['path', 'break_time', 'state']
    list_editable = ['state', 'msg']  # 设置可以直接在页面上编辑的字段


xadmin.site.register(Url_state, Url_stateAdmin)  # 将管理器注册


class UserOperateRecordAdmin(object):  # 注册DriverLicenseAdmin。注意，它继承的是object

    list_display = ['user', 'path', 'incident', 'count', 'creat_time_by_minutes', 'creat_time_by_day', 'run_time']
    search_fields = ['path', 'incident']
    list_filter = ['creat_time_by_minutes', 'creat_time_by_day']  # 添加过滤器功能


xadmin.site.register(UserOperateRecord, UserOperateRecordAdmin)  # 将管理器注册


class BombboxInfoAdmin(object):  # 注册BombboxInfoAdmin。注意，它继承的是object

    list_display = ['title', 'content', 'state']
    search_fields = ['title', 'content']
    list_filter = ['state']

    list_editable = ['title', 'state']  # 设置可以直接在页面上编辑的字段


xadmin.site.register(BombboxInfo, BombboxInfoAdmin)  # 将管理器注册
