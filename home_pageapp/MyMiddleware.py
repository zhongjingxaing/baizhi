from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("init1")

    def process_request(self, request):
        # 将需要放行的URL存储一个列表中
        pass_url = [reverse('loginapp:login'),reverse('loginapp:login_login'),reverse('registerapp:register'),reverse('registerapp:register_register'),reverse('registerapp:active')]
        # 如果请求路径 在 放行的URL的列表中
        if request.path not in pass_url:
            is_login = request.session.get('is_login')
            if is_login:
                pass
            else:
                return redirect('loginapp:login')
            # pass # 什么都不做
        else:
            pass  # 什么都不做
            # is_login = request.session.get('is_login')
            # if is_login:
            #     pass
            # else:
            #     return redirect('loginapp:login')