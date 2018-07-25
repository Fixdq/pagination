from django.shortcuts import render

from pagination import models
from utils import page


def index(request):
    # page　的使用
    # data = models.Book.objects.all()
    # page_current = request.GET.get('page')
    # page_obj = page.Pagination(page_current, data.count(), '/book_list/')
    # data_list = data[page_obj.start: page_obj.end]
    # return render(request, 'index.html', {'book_list': data_list, 'page_obj': page_obj})

    # page2 的使用
    data = models.Book.objects.all()
    page_current = request.GET.get('page')
    page_obj = page2.Pagination(page_current, data.count())
    data_list = data[page_obj.start:page_obj.end]
    return render(request, 'index.html', {'book_list': data_list, 'page_obj': page_obj})

