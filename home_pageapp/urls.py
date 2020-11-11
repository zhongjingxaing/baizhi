from django.urls import path
from home_pageapp import views

app_name="home_pageapp"


urlpatterns = [
   path('home/',views.home,name="home"),#进入主界面
   path('Reading_volume/',views.Reading_volume,name="Reading_volume"),#进行阅读量排序
   path('Reading_volume2/',views.Reading_volume2,name="Reading_volume2"),#进行阅读量和时间排序BASE界面
   path('updates/',views.updates,name="updates"),#进入更新页面
   path('updates_updates/',views.updates_updates,name="updates_updates"),#保存修改
   path('dell/',views.dell,name="dell"),#删除逻辑
   path('dell2/',views.dell2,name="dell2"),#删除逻辑
   path('logout/',views.logout,name="logout"),#进入退出登录界面
   path('addcourse/',views.addcourse,name="addcourse"),#进入增加课程及分类页面
   path('addaddcourse/',views.addaddcourse,name="addaddcourse"),#进入课程增加逻辑
   path('addarticle/',views.addarticle,name="addarticle"),#进入增加文章界面
   path('pythonbase/',views.pythonbase,name="pythonbase"),#进入课程分类的跳转界面
   path('Belonging_courses/',views.Belonging_courses,name="Belonging_courses"),#选择一级课程的下拉框找到二级下拉框
   path('addarticle_addarticle/',views.addarticle_addarticle,name="addarticle_addarticle"),#添加文章逻辑处理
   # path('delete/',views.delete,name="delete"),
]