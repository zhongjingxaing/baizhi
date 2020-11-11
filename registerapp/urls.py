from django.urls import path
from registerapp import views

app_name="registerapp"


urlpatterns = [
    path('get_captcha/',views.get_captcha,name="get_captcha"),#验证码
    path('register/',views.register,name="register"),#注册
    path('register_register/',views.register_register,name="register_register"),#注册逻辑
    path('usernames/',views.usernames,name="usernames"),#判断用户名是否符合2-10位中文
    path('pwdone/',views.pwdone,name='pwdone'),#判断第一个密码是否符合要求
    path('passwords/',views.passwords,name='passwords'),#判断密码是否在6-16位且符合要求
    path('active/',views.active,name="active"),#激活密码
    # path('register_logic/',views.register_logic,name='register_logic'),#判断验证码是否正确
]