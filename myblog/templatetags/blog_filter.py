from django.template import Library


# 注册
register = Library()


# 自定义过滤器,value是模板中的变量,num是后续的传参
# 自定义过滤器只能传一个参数
def mod(value, num):        # 取余
    return value % int(num)

register.filter('mod', mod)