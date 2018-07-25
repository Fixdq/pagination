from django.test import TestCase, Client


# Create your tests here.
class SimpleTest(TestCase):

    def test_list(self):
        # # 初始化数据
        # # 向数据库中插入1000条测试数据
        # from pagination import models
        #
        # # bulk_create: 批量插入
        # # 1.创建1000个对象
        # data = [models.Book(title="书籍--{}".format(i)) for i in range(1000)]
        # models.Book.objects.bulk_create(data)

        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('/index/', )
        self.assertEqual(response.status_code, 200)
