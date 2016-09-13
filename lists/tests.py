"""
    单元测试
"""

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # 方式一，每个元素都进行单独检测
        self.assertIn(b'<title>To-Do lists</title>',response.content)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertTrue(response.content.endswith(b'</html>'))
        self.assertIn(u"产品列表".encode('utf-8'),response.content)
        self.assertIn(b'<input name="item_text" id="id_new_item" placeholder="Enter a to-do item"/>',response.content)
        self.assertIn(u'购买'.encode('utf-8'),response.content)
        self.assertTrue(response.content.find(b'<button  class="btn btn-default dropdown-toggle" type="submit" data-toggle="dropdown">'))

        # 方式二，直接用render_to_string()函数进行直接全部页面进行检测

        expected_html = render_to_string('home.html',request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        '''
            在其中添加POST 请求，再检查返回的HTML 中是否有新添加的待办事项文本
        '''
        #设置测试的背景
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        #调用方法，最后编写断言
        response = home_page(request)

        #把POST请求中的数据存入数据库
        '''
        ➊、检查是否把一个新Item 对象存入数据库。objects.count() 是objects.all().count()的简写形式。
        ➋、 objects.first() 等价于objects.all()[0]。
        ➌、检查待办事项的文本是否正确。
        '''
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

#         #重定向
#         '''
#         不需要再拿响应中的.content 属性值和渲染模板得到的结果比较，因此把相应的断言删掉
# 了。现在，响应是HTTP 重定向，状态码是302，让浏览器指向一个新地址。
#         '''
#         self.assertEqual(response.status_code,302)
#         self.assertEqual(response['location'],'/')

        # self.assertIn('A new list item',response.content.decode())
        #
        # expected_html = render_to_string(
        #     'home.html',{'new_item_text':'A new list item',},request=request
        # )
        # print(expected_html)
        # print(response.content.decode())
        # self.assertEqual(response.content.decode(),expected_html)

    def test_home_redirects_after_POST(self):
        '''
        重定向
        '''
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_succssary(self):
        '''
        不要每次请求都保存空白的待办事项
        '''
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(),0)

    def test_home_page_displays_all_list_items(self):
        '''
        检查模板是否也能显示多个待办事项
        '''
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1',response.content.decode())
        self.assertIn('itemey 2',response.content.decode())

class ItemModelTest(TestCase):
    '''
    对象关系映射器
    由代码可以看出，在数据库中创建新记录的过程很简单：先创建一个对象，再为一些属
    性赋值，然后调用.save() 函数。Django 提供了一个查询数据库的API，即类属性.objects。
    再使用可能是最简单的查询方法.all()，取回这个表中的全部记录。得到的结果是一个类
    似列表的对象，叫QuerySet。从这个对象中可以提取出单个对象，然后还可以再调用其他函
    数，例如.count()。接着，检查存储在数据库中的对象，看保存的信息是否正确。
    '''
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
