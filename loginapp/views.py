from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from registerapp.models import TUser
from loginapp.captcha.image import ImageCaptcha
import string,random
import re
import hashlib
# Create your views here.


def login(request):#进入登录页面的html中
    username=request.COOKIES.get("username")
    password=request.COOKIES.get("password")
    if username:
        username = username.encode('latin-1').decode('utf-8')
        result=TUser.objects.filter(username=username,password=password)
        if result:
            return redirect('home_pageapp:home')
    return render(request,'login.html')

def usernames(request):#判断用户名是否存在
    name=request.POST.get('username')
    names=TUser.objects.get(username=name)
    name1 = re.match('^[\u4E00-\u9FA5]{2,10}$', name)
    if name1:
        if names:
            if names.is_active == 1:
                return HttpResponse("yes")  # 用户名存在
            return HttpResponse('nono')
        return HttpResponse("no")#用户名不存在
    return HttpResponse("cuo")#用户名应是2-10位的纯中文组成

def passwords(request):#判断密码是否正确
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=TUser.objects.get(username=username)
    print(user.password)
    if user:
        sha = hashlib.md5()
        salt = user.salt
        sha.update((password + salt).encode())
        pwd = sha.hexdigest()  # 加盐后的密码进行比对

        if user.password==pwd:
            return HttpResponse("yes")#密码正确
        return HttpResponse("no")#密码错误
    return HttpResponse("noo")

    # if user:


def login_login(request):#进入登录逻辑判断是否符合登录条件
    username=request.POST.get("username")
    password=request.POST.get("password")
    rem = request.GET.get("remember")
    print(998,username,password,rem)

    name1 = re.match('^[\u4E00-\u9FA5]{2,10}$', username)
    user = TUser.objects.get(username=username)

    if user:
        sha = hashlib.md5()
        salt=user.salt
        sha.update((password+salt).encode())
        pwd=sha.hexdigest()#加盐后的密码进行比对

        if name1:#符合正则
            if user.is_active == 1:#激活状态
                if user.password == pwd:

                    resp= HttpResponse("yes")
                    if rem:
                        username = username.encode('utf-8').decode('latin-1')  # 处理中文问题
                        resp.set_cookie('username', username, max_age=3600 * 24 * 7)
                        resp.set_cookie('password', password, max_age=3600 * 24 * 7)
                    request.session['is_login']=True
                    request.session['username'] =username
                    return resp  # 进入主页
                return HttpResponse('no')  # 密码不正确
            return HttpResponse('nono')#用户没有被激活
        return HttpResponse("noo")#用户名不符合规范
    else:
        return HttpResponse("用户不存在")
