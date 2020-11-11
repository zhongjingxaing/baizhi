import traceback

from django.core.paginator import Paginator
from datetime import datetime

from django.db import transaction
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.urls import reverse

from home_pageapp.models import TArticle#文章内容表
from home_pageapp.models import TCategory#课程分类表

import json
# Create your views here.



def dell(request):  # 主页面删除用户的一行信息
    id = request.GET.get('id')
    print(1181,id)
    user = TArticle.objects.get(id=id)
    user.delete()
    return redirect('home_pageapp:home')
    # return HttpResponse('111')

def dell2(request):  # base界面删除用户的一行信息
    id = request.GET.get('id')
    print(id)
    user = TArticle.objects.get(id=id)
    user.delete()
    return redirect('home_pageapp:home')

def home(request):
    writ=TArticle.objects.all()#获取全部文章
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    yue=request.GET.get('yue')

    if yue=="1":
        writ = TArticle.objects.all().order_by("count")  # 获取全部文章
    title1=TCategory.objects.filter(level=1)#获取一级标题
    title2=TCategory.objects.filter(level=2)#获取一级标题
    is_login = request.session.get('is_login')

    number = int(request.GET.get('number', 1))
    if is_login==True:
        # 声明分页器对象
        pagtor = Paginator(object_list=writ, per_page=5)
        # 判断页号是否存在

        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)

        return render(request, 'index.html',{'page': page,"writ":writ,"title1":title1,"title2":title2,"number":number}) # 传到HTML中一级标题
    return redirect('loginapp:login')

def logout(request):#退出登录
    return render(request,'logout.html')#退出登录  退出时需要将记住我密码清掉


def addcourse(request):#进入增加课程类界面
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    cates = TCategory.objects.filter(level=1)  # 课程类别一级标题
    sub_cates = TCategory.objects.filter(level=2)  # 课程名称二级标题
    return render(request,'addCourse.html',{"cates":cates,"sub_cates":sub_cates})#进入增加课程分类页面

def addaddcourse(request):#进入增加课程逻辑
    try:
        name = request.POST.get("name")
        title = request.POST.get("title")
        course_name = request.POST.get("cate_sel")
        print(161,name,title,course_name)
        with transaction.atomic():
            print(11,course_name)
            if course_name == None:
                TCategory.objects.create(title=name, level=int(title))
                return HttpResponse("yes")
                print(22,course_name)
            elif course_name == "defaultCate":
                return HttpResponse("no")
            else:
                parend_id = TCategory.objects.get(title=course_name).id
                print(33,parend_id)
                TCategory.objects.create(title=name, level=int(title), parent_id=parend_id)
                return HttpResponse("yes")
    except:
        traceback.print_exc()
        return HttpResponse("no")

def addarticle(request):#进入添加文章页面
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    articles = TArticle.objects.all()  # 获取全部文章
    cates = TCategory.objects.filter(level=1)  # 获取一级标题
    sub_cates = TCategory.objects.filter(level=2)  # 获取二级标题
    return render(request,'addArticle.html',{"cates":cates,"sub_cates":sub_cates,"articles":articles})

def Belonging_courses(request):#通过所属课程的id 获取库中对应的二级课程
    list=[]
    id = request.POST.get('id')  # 获取文章所属课程的一级标题的id
    if id:
        sub_cate = TCategory.objects.filter(parent_id=id)  # 与所选课程对应的二级课程的Querset对象
        for i in sub_cate:
            list.append(i.title)
    return HttpResponse(json.dumps(list), content_type='application/json')

def addarticle_addarticle(request):
    try:
        biao=request.POST.get('title')#获取到的文章标题
        title1=request.POST.get('title1')#获取二级标题的title
        tims1=request.POST.get('my_time')#获取时间
        text=request.POST.get('form_control')#获取文章内容
        title=TCategory.objects.get(title=title1)
        # titles = TCategory.objects.get(title=title)#获取文章标题
        cate_id=title.id#得出文章的cate_id
        print(1111,biao,title1,tims1,text,cate_id)
        TArticle.objects.create(title=biao, content=text, cate_id=int(cate_id),publish_time=tims1)#写入库中
        return HttpResponse('yes')
    except:
        return HttpResponse('no')

def pythonbase(request):
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    articles = TArticle.objects.all()  # 获取全部文章

    cates = TCategory.objects.filter(level=1)  # 获取一级标题
    sub_cates = TCategory.objects.filter(level=2)  # 获取二级标题

    id=request.GET.get('id')


    print(888,id,type(id))
    level=request.GET.get('level')
    is_login = request.session.get('is_login')
    if is_login==True:
        if level=="1":
            title1 =cates.filter(id=id)[0].title
            title2=''
            articles = TArticle.objects.filter(cate__parent_id=id)
        else:
            articles = TArticle.objects.filter(cate=id)
            # id9 = TCategory.objects.filter(id=id)[0].parent_id
            # print(id9,9696)
            title1=TCategory.objects.filter(id=TCategory.objects.filter(id=id)[0].parent_id)[0].title#传出标题
            title2=sub_cates.filter(id=id)[0].title

        print(19, articles)
        # 获取url中的参数，如果不存在返回第1页
        number = int(request.GET.get('number', 1))
        type1 = TCategory.objects.filter(level=1)
        type2 = TCategory.objects.filter(level=2)
        # 声明分页器对象
        pagtor = Paginator(object_list=articles, per_page=5)

        # 判断页号是否存在
        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)
        # 向后端传递的是页面对象
        # return render(request, 'uploadapp/userlist.html', {'page': page})
        print(111,id)
        id1=int(id)
        dict={"title1": title1, "title2": title2,"writ": articles,'page': page,"cates": cates,
                                                   "sub_cates": sub_cates,"articles":articles,
                                                   "level":level,'type1':type1,"id":id,"id1":id1,
                                               'type2':type2}
      # "title1": title1, "title2": title2,
        return render(request, 'pythonBase.html', dict)


def updates(request):
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    id=request.GET.get('id')
    title = request.GET.get('title')
    cate_id=request.GET.get('cate_id')

    d3=TArticle.objects.get(id=id)#获取库中的文章标题的id
    d2 = TCategory.objects.get(id=d3.cate_id) # 获取库中的二级标题的id
    d1 = TCategory.objects.get(id=d2.parent_id)#获取库中的一级标题对象

    articles = TArticle.objects.all()  # 获取全部文章
    cates = TCategory.objects.filter(level=1)  # 获取一级标题
    sub_cates = TCategory.objects.filter(level=2)  # 获取二级标题
    print(1,id,2,title,3,cate_id,4,articles,5,cates,6,sub_cates)
    return render(request, 'update.html', {"d1":d1,"d2":d2,"d3":d3,"title":title,"cates": cates, "sub_cates": sub_cates, "articles": articles})
def updates_updates(request):
    try:
        biao=request.POST.get('title')#获取到的文章标题
        title1=request.POST.get('title1')#获取二级标题的title
        tims1=request.POST.get('my_time')#获取时间

        text=request.POST.get('form_control')#获取文章内容
        title=TCategory.objects.get(title=title1)
        cate_id=title.id#得出文章的cate_id
        print(1111,biao,title1,tims1,text,title,cate_id)
        TArticle.objects.create(title=biao, content=text, cate_id=int(cate_id),publish_time=tims1,count= 1)#写入库中
        return HttpResponse('yes')
    except:
        return HttpResponse('no')


def Reading_volume(request):

    yue = request.GET.get('yue')
    # times = request.GET.get('yue')
    if yue:
        writ = TArticle.objects.all().order_by('-count')#获取全部文章
        title1 = TCategory.objects.filter(level=1)  # 获取一级标题
        title2 = TCategory.objects.filter(level=2)  # 获取一级标题

        number = int(request.GET.get('number', 1))
            # 声明分页器对象
        pagtor = Paginator(object_list=writ, per_page=5)
        # 判断页号是否存在

        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)

        return render(request, 'index.html',
                      {'page': page, "writ": writ, "title1": title1, "title2": title2, "number": number})  # 传到HTML中一级标题
    else:
        writ = TArticle.objects.all().order_by('-publish_time')  # 获取全部文章
        title1 = TCategory.objects.filter(level=1)  # 获取一级标题
        title2 = TCategory.objects.filter(level=2)  # 获取一级标题

        number = int(request.GET.get('number', 1))
        # 声明分页器对象
        pagtor = Paginator(object_list=writ, per_page=5)
        # 判断页号是否存在

        if number not in pagtor.page_range:
            number = 1
        page = pagtor.page(number)

        return render(request, 'index.html',
                      {'page': page, "writ": writ, "title1": title1, "title2": title2, "number": number})  # 传到HTML中一级标题
def Reading_volume2(request):
    # username = request.COOKIES.get('username')
    # username = username.encode('latin-1').decode('utf-8')
    yue = request.GET.get('yue')
    # times = request.GET.get('yue')
    if yue:
        cates = TCategory.objects.filter(level=1)  # 获取一级标题
        sub_cates = TCategory.objects.filter(level=2)  # 获取二级标题
        id=request.GET.get('id')
        print(888,id,type(id))
        level=request.GET.get('level')
        is_login = request.session.get('is_login')
        if is_login==True:
            if level=="1":
                title1 =cates.filter(id=id)[0].title
                title2=''
                articles = TArticle.objects.filter(cate__parent_id=id).order_by('-count')
            else:
                articles = TArticle.objects.filter(cate=id).order_by('-count')
                title1=TCategory.objects.filter(id=TCategory.objects.filter(id=id)[0].parent_id)[0].title#传出标题

                title2=sub_cates.filter(id=id)[0].title
            # 获取url中的参数，如果不存在返回第1页
            number = int(request.GET.get('number', 1))
            type1 = TCategory.objects.filter(level=1)
            type2 = TCategory.objects.filter(level=2)
            # 声明分页器对象
            pagtor = Paginator(object_list=articles, per_page=5)
            # 判断页号是否存在
            if number not in pagtor.page_range:
                number = 1
            page = pagtor.page(number)
            print(111,id)
            id1=int(id)
            dict={"title1": title1, "title2": title2,"writ": articles,'page': page,"cates": cates,
                                                       "sub_cates": sub_cates,"articles":articles,
                                                       "level":level,'type1':type1,"id":id,"id1":id1,
                                                   'type2':type2}
          # "title1": title1, "title2": title2,
            return render(request, 'pythonBase.html', dict)
    else:
        cates = TCategory.objects.filter(level=1)  # 获取一级标题
        sub_cates = TCategory.objects.filter(level=2)  # 获取二级标题
        id = request.GET.get('id')
        print(888, id, type(id))
        level = request.GET.get('level')
        is_login = request.session.get('is_login')
        if is_login == True:
            if level == "1":
                title1 = cates.filter(id=id)[0].title
                title2 = ''
                articles = TArticle.objects.filter(cate__parent_id=id).order_by('-publish_time')
            else:
                articles = TArticle.objects.filter(cate=id).order_by('-publish_time')
                title1 = TCategory.objects.filter(id=TCategory.objects.filter(id=id)[0].parent_id)[0].title  # 传出标题
                title2 = sub_cates.filter(id=id)[0].title
            # 获取url中的参数，如果不存在返回第1页
            number = int(request.GET.get('number', 1))
            type1 = TCategory.objects.filter(level=1)
            type2 = TCategory.objects.filter(level=2)
            # 声明分页器对象
            pagtor = Paginator(object_list=articles, per_page=5)
            # 判断页号是否存在
            if number not in pagtor.page_range:
                number = 1
            page = pagtor.page(number)
            print(111, id)
            id1 = int(id)
            dict = {"title1": title1, "title2": title2, "writ": articles, 'page': page, "cates": cates,
                    "sub_cates": sub_cates, "articles": articles,
                    "level": level, 'type1': type1, "id": id, "id1": id1,
                    'type2': type2}
            # "title1": title1, "title2": title2,
            return render(request, 'pythonBase.html', dict)