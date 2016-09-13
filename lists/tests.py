"""
    单元测试
"""

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page

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