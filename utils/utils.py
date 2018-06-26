#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-6-26 下午5:08
# @Author  : fixdq
# @File    : utils.py
# @Software: PyCharm


class Pagination(object):
    def __init__(self, page_current, data_total, base_url, page_show_num=10, page_index_show_num=11):
        """

        :param page_current: 当前页码
        :param data_total: 数据总条数
        :param base_url: 显示数据的url
        :param page_show_num: 每页显示多少数据 默认是10条
        :param page_index_show_num: 菜单页显示的个数

        使用方式：
            # 查询所有书籍
            data = models.Book.objects.all()
            page_current = request.GET.get('page')
            pag_obj = utils.pagination(page_current, data.count(), '/book_list/')
            data_list = data[pag_obj.start: pag_obj.end]
            return render(request, 'book_list.html', {'book_list': data_list, 'li_data': pag_obj.page_html()})

        """
        # 获取显示的页码
        try:
            self.page_current = int(page_current)
        except Exception as e:
            # 页码输入不正确设置当前页为 首页
            self.page_current = 1
        # 查询所有书籍
        self.data_total = data_total
        self.base_url = base_url
        self.page_show_num = page_show_num
        self.page_index_show_num = page_index_show_num
        # 计算出前后页码显示的个数
        self.half_page_index_show_num = page_index_show_num // 2
        # 当前总共需要多少页码
        page_total, more = divmod(self.data_total, page_show_num)
        # 如果有余数 就把页码数+1
        self.page_total = page_total if not more else page_total + 1

    @property
    def start(self):
        return (self.page_current - 1) * self.page_show_num

    @property
    def end(self):
        return self.page_current * self.page_show_num+1

    def page_html(self):

        if self.page_current - self.half_page_index_show_num <= 1:
            page_start = 1  # 开始页为第一页
            page_end = self.page_index_show_num  # 结束页为显示页码的长度
        elif self.page_total - self.page_current <= self.half_page_index_show_num:
            page_start = self.page_total - self.page_index_show_num + 1
            page_end = self.page_total
        else:
            page_start = self.page_current - self.half_page_index_show_num
            page_end = self.page_current + self.half_page_index_show_num

        # 定义存储li的列表
        li_list = []

        # 添加首页
        li_list.append('<li><a href="{base_url}?page=1">首页</a></li>'.format(base_url=self.base_url))
        # 添加上一页
        if self.page_current <= 1:  # 第一页 禁用上一页按钮
            pre_html = '<li class="disabled"><a ><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            pre_html = '<li ><a href="{base_url}?page={page}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                page=self.page_current - 1, base_url=self.base_url)
        li_list.append(pre_html)
        # 生成所有显示的页码

        for i in range(page_start, page_end + 1):
            if i == self.page_current:
                cur_html = '<li class="active"><a href="{base_url}?page={page}">{page}</a></li>'.format(
                    page=i, base_url=self.base_url)
            else:
                cur_html = '<li ><a href="{base_url}?page={page}">{page}</a></li>'.format(page=i,
                                                                                          base_url=self.base_url)
            li_list.append(cur_html)

        # 添加下一页
        if self.page_current >= self.page_total:  # 最后一页 禁用下一页按钮
            next_html = '<li class="disabled"><a ><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            next_html = '<li ><a href="{base_url}?page={page}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                page=self.page_current + 1, base_url=self.base_url)
        li_list.append(next_html)
        # 添加尾页
        li_list.append(
            '<li><a href="{base_url}?page={page}">尾页</a></li>'.format(page=self.page_total, base_url=self.base_url))

        return ''.join(li_list)
