# LOG

## 日志模块
由我自己单独维护的一个app，可直接由任何项目使用。

*  日志程序位置：error_Traceback
*  具体的函数及功能：  
    *  log_exception：记录程序发生错误时的堆栈信息。  
        相关文件有两个：
    *  request_error.log：每发生一次错误，记录一个500错误。例子如下：  
                        
                2017-10-26 17:35:07 [ERROR] [5082.Thread-3:123145453871104] [error_Traceback.wrap] -- "GET /get_user_info HTTP/1.1" 500
    *  error_Traceback.log：发生错误的同时，记录当时的堆栈信息，方便查错。不再举例。

## 使用方式
*  把 log_exception 直接通过装饰器的方式加在所需要记录日志的程序代码上。但是有三个要求：
    *  需要装饰的程序代码必须是项目url对应的类或方法。
    *  整个程序内最好不要有Try——except模块，因为需要用log_exception记录错误。
    *  方法中的第一个参数必须是request（除self）。例如:

            @log_exception
            def jsapi_signature(request):
                ...

            @method_decorator(log_exception, name='get')
            @method_decorator(log_exception, name='post')
            class get_user_info(View):
                def get(self, request):
                        ...
                def post(self, request):
                        ...
                    
## 发件原理
* 第一种发件模式：直接发送，需要配置setting文件，配置如下：

		# QQ邮箱
		EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  #email后端
		EMAIL_USE_TLS = False   #是否使用TLS安全传输协议
		EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用
		EMAIL_HOST = 'smtp.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了qq企业邮箱
		EMAIL_PORT = 465     #发件箱的SMTP服务器端口
		EMAIL_HOST_USER = '1943336161@qq.com'    #发送邮件的邮箱地址
		EMAIL_HOST_PASSWORD = 'eztqbvljzyokgbae'         #发送邮件的邮箱密码
		DEFAULT_FROM_EMAIL = '叶孟豪<1943336161@qq.com>'
	另外，还需要对django的log进行配置，见log_setting.py文件。

* 第二种发件模式：代理发送，向指定API发送请求，由已经配置好的服务器进行发送。

## 其他相关
>生成依赖：pip freeze > requirements.txt  
安装依赖：pip install -r requirements.txt
