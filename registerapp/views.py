import token
import uuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from registerapp.models import TUser
from loginapp.captcha.image import ImageCaptcha
import string, random
import re
import hashlib

# Create your views here.
# Create your views here.
def get_captcha(request):
    # 声明一个图片验证码对象
    image = ImageCaptcha()
    # 生成随机验证码
    code = random.sample(string.ascii_letters + string.digits, 4)
    code = ''.join(code)
    print(code)
    # 将验证码写到图片中
    data = image.generate(code)  # 返回:二进制数据
    # 存储seccion
    request.session['code'] = code
    return HttpResponse(data, 'image/png')

def register(request):  # 进入注册页面
    return render(request, 'register.html')

def active(request):
    try:#账户激活
        token=request.GET.get('token')
        ser = Serializer(settings.SECRET_KEY, expires_in=3600)
        id = ser.loads(token).get('id')
        user = TUser.objects.get(pk=id)
        user.is_active = 1
        user.save()
        return HttpResponse("激活成功")
    except:
        return HttpResponse("激活码已过期")
def register_register(request):  # 进入注册逻辑
    # try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        captcha = request.POST.get('captcha')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        users = TUser.objects.filter(username=username)
        print(username, password, password1, captcha, email, allow,9999)
        if users:
            return HttpResponse("存在")
            # return HttpResponse('1')#用户已存在
        else:
            if password != password1:
                pass
                # return HttpResponse('2')#密码不一致
            else:
                name1=re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email)
                print(name1)
                if name1:
                    print("进入验证了")
                    print(captcha)
                    print(request.session.get('code').lower())
                    if captcha.lower() == request.session.get('code').lower():
                        print("进入到验证码了")
                        if allow:
                            print("来存储信息了")

                            salt = str(uuid.uuid4())#加盐操作
                            sha = hashlib.md5()
                            sha.update((password+salt).encode())
                            pwd = sha.hexdigest()  # 进行密码加密操作

                            #对id进行加密操作
                            user=TUser.objects.create(username=username, password=pwd, email=email,salt=salt)
                            ser = Serializer(settings.SECRET_KEY, expires_in=3600)
                            result = ser.dumps({'id': user.id})
                            send_mail('邮件主题', f'用户:{username}请求激活帐号，链接为：http://127.0.0.1:8000/registerapp/active/?token='+result.decode('utf-8'),'2327260230@qq.com',['1942263848@qq.com'])

                            return HttpResponse("ok")
                        return HttpResponse('1')#未勾选协议
                    print("验证码不一致")
                    return HttpResponse("2")#验证码不一致
                print("用户名不合法")
def usernames(request):  # 判断用户名是否存在
    name = request.POST.get('username')
    re = TUser.objects.filter(username=name)
    if re:
        return HttpResponse("no")  # 用户名已存在
    else:
        return HttpResponse("yes")  # 用户名合法

def pwdone(request):  # 判断确认密码是否在6-18位
    password = request.POST.get('password')
    print(password)
    if password != '':
        if len(password) >= 6 and len(password) <= 16:
            return HttpResponse('yes')  # 密码合格
        return HttpResponse("no")  # 密码长度应在6-16位
    else:
        return HttpResponse('nn')  # 密码不能为空


def passwords(request):  # 判断确认第二次密码是否在6-18位
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    print(password1, password)
    if password != '' and password1 != '':
        if password1 == password:
            if len(password) >= 6 and len(password) <= 16:
                return HttpResponse('yes')  # 密码合格

            return HttpResponse("no")  # 密码长度应在6-16位
        else:
            return HttpResponse("nono")  # 密码不一致
    else:
        return HttpResponse('nn')  # 密码不能为空

#
def register_logic(request):
    captcha = request.POST.get('captcha')
    if captcha.lower() == request.session.get('code').lower():
        # ...
        return HttpResponse('yes')
    return HttpResponse('no')
