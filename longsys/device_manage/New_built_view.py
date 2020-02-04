from django.views.generic import ListView


class New_Built_View(ListView):
    """ 继承ListView"""
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)