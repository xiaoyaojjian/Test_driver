# Test_driver
测试驱动练习

第四章：
1、render_to_string()使用
  django1.9需加上render_to_string()参数中request=request,否则报错
2、render()使用
3、进行response.content比较使用的原字节码转换,如：遇到中文进行比较
  self.assertIn(u'购买'.encode('utf-8'),response.content)
4、assertIN()\assertEqual()\assertTrue()使用

  
