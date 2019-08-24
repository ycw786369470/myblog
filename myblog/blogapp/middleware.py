# 10.版本以上django需导入
# from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


class MyMiddleware():
    # 初始化，第一次请求的时候执行
    def __init__(self):
        print('init执行咯')

    '''
        执行场景:封ip、拒绝访问等
        执行位置:构造好请求之后，匹配视图之前，返回none将继续执行
        如果返回HttpResponse对象则直接返回浏览器
        :param request:
        :return:
    '''
    def process_request(self, request):
        # 设置ip黑名单
        black_list = ['127.0.0.1']
        # 获取当前请求对象的ip
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip in black_list:
            return HttpResponse('???Eat shit spder-man???')
        print('process_request执行咯')


    '''
        执行位置：配置视图之后，执行视图之前
        :param request: 请求对象
        :param view_func: 视图函数
        :param view_args: 视图函数的位置参数
        :param view_kwargs: 视图函数的关键字参数
        :return: 反回None就继续执行视图函数，如果返回HttpResponse对象则直接返回浏览器
    '''
    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view执行咯')

    '''
        执行位置：执行完视图之后，处理模板相应之前
    '''
    def process_template_response(self, request, response):
        print('process_template_response执行咯')

    '''
        
    '''
    def process_response(self, request, response):
        print('process_response执行咯')


    '''
    
    '''
    def process_exception(self, request, response):
        print('process_exception执行咯')







