import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "page.settings")
    import django
    django.setup()

    # 向数据库中插入1000条测试数据
    from pagination import models

    # bulk_create: 批量插入
    # 1.创建1000个对象
    data = [models.Book(title="书籍--{}".format(i)) for i in range(1000)]
    models.Book.objects.bulk_create(data)
