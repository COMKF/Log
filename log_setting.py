# TODO 注意log文件要写在服务器系文件系统中，部署前要修改路径
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'illegal_query': {
            'format': "%(asctime)s,%(message)s,%(car_id)s,%(brand)s,%(user_id)s,%(user_op)s,%(fkje)s,%(clbj)s,%(wfjfs)s,%(wfdz)s,%(wfxw)s,%(wfsj)s,%(user_op_id)",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'standard': {
            'format': "%(asctime)s|%(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(pathname)s %(lineno)d %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'syslog': {
            'format': "%(asctime)s [%(levelname)s] [%(process)d.%(threadName)s:%(thread)d] [%(module)s.%(funcName)s] -- %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {  # 控制台
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'filters': ['require_debug_true'],
            'formatter': 'syslog'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['require_debug_false'], # 仅当 DEBUG = False 时才发送邮件
        },
        'request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': '/var/log/wxlog/syslog/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.syslog',
            'filename': 'request.log',
            'maxBytes': 1024 * 1024 * 64,  # 64M
            'backupCount': 2,
            'formatter': 'syslog',
        },
        'request_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': '/var/log/wxlog/syslog/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.syslog',
            'filename': 'request_error.log',
            'maxBytes': 1024 * 1024 * 64,  # 64M
            'backupCount': 2,
            'formatter': 'syslog',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': '/var/log/wxlog/syslog/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.syslog',
            'filename': 'db.log',
            'maxBytes': 1024 * 1024 * 64,  # 64M
            'backupCount': 2,
            'formatter': 'syslog',
        },
        'exception_log': {
            'level': 'DEBUG',  # 打印DEBUG （或更高）级别的消息。
            'class': 'logging.handlers.RotatingFileHandler',  # 它的主体程序是RotatingFileHandler类，这是最重要的。
            'filename': "error_Traceback.log",
            'maxBytes': 1024 * 1024 * 1024,  # 每个日志文件大小
            'backupCount': 2,
            'formatter': 'verbose',  # 采用verbose为格式化器。
        },
        '214_error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 它的主体程序是RotatingFileHandler类，这是最重要的。
            'filename': "214_error.log",
            'maxBytes': 1024 * 1024 * 1024,  # 每个日志文件大小
            'backupCount': 2,
            'formatter': 'verbose',  # 采用verbose为格式化器。
        },
        'from_214_back_error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 它的主体程序是RotatingFileHandler类，这是最重要的。
            'filename': "from_214_back_error.log",
            'maxBytes': 1024 * 1024 * 1024,  # 每个日志文件大小
            'backupCount': 2,
            'formatter': 'verbose',  # 采用verbose为格式化器。
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     'propagate': False,
        #     'level': 'DEBUG',
        # },
        'django.server': {
            'handlers': ['request', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_server_log': {
            'handlers': ['request_error'],
            'level': 'INFO',
            'propagate': True,
        },
        'exception_log': {
            'handlers': ['exception_log'],
            'level': 'ERROR',
        },
        '214_error': {
            'handlers': ['214_error'],
            'level': 'WARNING',
        },
        'from_214_back_error': {
            'handlers': ['from_214_back_error'],
            'level': 'WARNING',
        },
    }
}
