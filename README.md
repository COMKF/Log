# LOG
由我自己单独维护的一个app，可直接由任何项目使用。

## 异常报警模块
###  程序位置：utils.error_Traceback
###	另外，还需要对django的log进行配置，见log_setting.py文件。

###  具体的函数及功能：  
*  log_exception：程序发生错误时的处理程序，相关日志文件有两个：
	*  request_error.log：每发生一次错误，记录一个500错误。例子如下：  
	                    
	            2017-10-26 17:35:07 [ERROR] [5082.Thread-3:123145453871104] [error_Traceback.wrap] -- "GET /get_user_info HTTP/1.1" 500
	*  error_Traceback.log：发生错误的同时，记录当时的堆栈信息，方便查错。不再举例。

### 使用方式
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
                        
## 用户行为记录模块
###  程序位置：utils.UserOperateUtils
###  具体的函数及功能：  
*  log_user_operate：用户访问项目时，记录相关的信息，保存到数据库中，相关的model有一个：
	*  UserOperateRecord：记录内容详见model表。

### 使用方式
*  把 log_user_operate 直接通过装饰器的方式加在所需要记录用户行为的程序代码上。要求和上面 log_exception 一样，用法也一样。

## url控制模块
###  程序位置：utils.check_url
###  具体的函数及功能： 
*  check_url_state：以url为主，控制url状态，方便随时挂维护，相关的model有一个：
	*  Url_state：记录内容详见model表。

### 使用方式
*  把 check_url_state 直接通过装饰器的方式加在所需要记录用户行为的程序代码上。要求和上面 log_exception 一样，用法也一样。

## 附：弹框模块
###  程序位置：views.GetBombboxInfo；views.CancelBombboxInfo；
###  具体的函数及功能： 
*  功能：以url请求的方式，调用保存在数据库中的弹框信息，做到一个简易的用户通知，同时用户可以取消弹框显示，相关的model有两个：
	*  BombboxInfo：页面弹框信息，记录内容详见model表。
	*  CancelBombboxInfoRecord：取消弹框记录，记录内容详见model表。

### 使用方式
*  需要前端向服务器发送post请求，获取弹框信息，弹出confirm弹框，根据用户的不同行为，进行不同的操作。前端示例代码如下（Log app中无此段代码）：

	      this.$axios.post('/alipay/GetBombboxInfo/').then(response => {
	        if (response.data.ok) {
	          let title = response.data.title
	          let content = response.data.content
	          let Bombbox_info_id = response.data.Bombbox_info_id
	          self.$ready(function () {
	            AlipayJSBridge.call('confirm', {
	              title: title,
	              message: content,
	              okButton: '我知道了',
	              cancelButton: '不再提醒'
	            }, function (e) {
	              if (e.ok) {
	              } else {
	                self.$axios.post('/alipay/CancelBombboxInfo/', {Bombbox_info_id: Bombbox_info_id}).then(response => {
	                })
	              }
	            })
	          })
	        }
	      })
* 后端代码见 url 和上面的程序位置。
                    
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

* 第二种发件模式：代理发送，向指定API发送请求，由已经配置好的服务器进行发送。

## 


## 其他相关
>生成依赖：pip freeze > requirements.txt  
安装依赖：pip install -r requirements.txt
