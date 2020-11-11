from django.urls import path
from loginapp import views

app_name="loginapp"


urlpatterns = [
    path('login/',views.login,name="login"),#登录
    path('login_login/',views.login_login,name="login_login"),
    path ('usernames/',views.usernames,name='usernames'),#判断用户是否存在
    path('passwords/',views.passwords,name="passwords"),#判断用户密码是否一致,



]