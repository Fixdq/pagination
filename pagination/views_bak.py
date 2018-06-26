from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from app01 import models


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
    # 获取显示的页码
    try:
        page_current = int(request.GET.get('page'))
    except Exception as e:
        # 页码输入不正确设置当前页为 首页
        page_current = 1
    # 查询所有书籍
    data = models.Book.objects.all()

    # 数据总条数
    data_total_rows = data.count()
    # 每页显示条数
    page_show_num = 20
    # 对应页显示的数据
    data_list = data[(page_current - 1) * page_show_num:page_current * page_show_num]

    # 当前总共需要多少页码
    page_total, more = divmod(data_total_rows, page_show_num)
    # 如果有余数 就把页码数+1
    page_total = page_total if not more else page_total + 1

    # 处理页码最前端和最后端的问题
    # 如果当前页大于总页数 显示为最有一个总页数
    if page_current >= page_total:
        page_current = page_total
    # 如果当前页 小于 1   显示为第一页
    if page_current <= 1:
        page_current = 1

    # 求页面上 展示的页码范围
    page_index_show_num = 7
    # 计算出前后页码显示的个数
    half_page_index_show_num = page_index_show_num // 2

    if page_current - half_page_index_show_num <= 1:
        page_start = 1  # 开始页为第一页
        page_end = page_index_show_num  # 结束页为显示页码的长度
    elif page_total - page_current <= half_page_index_show_num:
        page_start = page_total - page_index_show_num + 1
        page_end = page_total
    else:
        page_start = page_current - half_page_index_show_num
        page_end = page_current + half_page_index_show_num
    """
    <ul class="pagination">
        <li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
        <li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>
        <li><a href="#">2</a></li>
        <li><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
     </ul>
    """
    # 定义存储li的列表
    li_list = []

    # 添加首页
    li_list.append('<li><a href="/book_list/?page=1">首页</a></li>')
    # 添加上一页
    if page_current <= 1:  # 第一页 禁用上一页按钮
        pre_html = '<li class="disabled"><a ><span aria-hidden="true">&laquo;</span></a></li>'
    else:
        pre_html = '<li ><a href="/book_list/?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
            page_current - 1)
    li_list.append(pre_html)
    # 生成所有显示的页码

    for i in range(page_start, page_end + 1):
        if i == page_current:
            cur_html = '<li class="active"><a href="/book_list/?page={0}">{0}</a></li>'.format(
                i)
        else:
            cur_html = '<li ><a href="/book_list/?page={0}">{0}</a></li>'.format(i)
        li_list.append(cur_html)

    # 添加下一页
    if page_current >= page_total:  # 最后一页 禁用下一页按钮
        next_html = '<li class="disabled"><a ><span aria-hidden="true">&raquo;</span></a></li>'
    else:
        next_html = '<li ><a href="/book_list/?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
            page_current + 1)
    li_list.append(next_html)
    # 添加尾页
    li_list.append('<li><a href="/book_list/?page={}">尾页</a></li>'.format(page_total))

    li_data = ''.join(li_list)
    return render(request, 'book_list.html', {'book_list': data_list, 'li_data':  li_data})


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
