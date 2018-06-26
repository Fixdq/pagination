from django.shortcuts import render, redirect

from pagination import models
from utils import utils


def check_login(func):
    def inner(request, *args, **kwargs):
        # 判断用户是否登录
        res = request.session.get('user')
        url = request.path_info
        # print(url)
        if not res:
            return redirect('/login/?url={}'.format(url))
        else:
            return func(request, *args, **kwargs)

    return inner


@check_login
def book_list(request):
    # 查询所有书籍
    data = models.Book.objects.all()
    page_current = request.GET.get('page')
    pag_obj = utils.Pagination(page_current, data.count(), '/book_list/')
    data_list = data[pag_obj.start: pag_obj.end]
    return render(request, 'book_list.html', {'book_list': data_list, 'li_data': pag_obj.page_html()})


def login(request):
    err_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = models.User.objects.filter(username=username, pwd=pwd)

        if user:
            # 登录成功
            # 生成随机字符串，开辟空间，保存session
            print('success')
            request.session['user'] = username
            # 判断是否是从其他url跳转过来的登录
            target_url = request.GET.get('url', '')
            print(target_url)
            if target_url:
                red = target_url
            else:
                red = '/index/'
            return redirect(red)
        else:
            err_msg = '登录错误'

    return render(request, 'login.html', {'err_msg': err_msg})


def index(request):
    return render(request, 'index.html')


def logout(request):
    request.session.flush()
    return redirect('/login/')
