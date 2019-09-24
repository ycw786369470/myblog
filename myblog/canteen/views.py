from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from blogapp.models import *


# Create your views here.
def choose_name(request):
    if request.method == 'POST':
        canteen_num = str(request.POST.get('name'))
        # 拉取餐厅信息,拉取失败则返回选择页面
        try:
            cantee = Canteen.objects.get(canteen_num=canteen_num)
            request.session['canteen_num'] = canteen_num
        except:
            return render(request, 'canteen/choose_name.html', {'canteen_num': canteen_num,
                                                                'warming': 1,
                                                                })
        return HttpResponseRedirect('/canteen/table/')
    elif request.method == 'GET':
        return render(request, 'canteen/choose_name.html')


def choose_table(request):
    if request.method == 'GET':
        canteen_num = request.session.get('canteen_num')
        print(canteen_num)
        canteen = Canteen.objects.get(canteen_num=canteen_num)
        tables = Table.objects.get(canteen=canteen)
        return render(request, 'canteen/choose_table.html')