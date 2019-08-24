from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(BlogUser)
admin.site.register(Mark)
admin.site.register(Users)
admin.site.register(Upload)
admin.site.register(Sentence)
admin.site.register(NewBlog)
admin.site.register(Message)
admin.site.register(FriendLink)
admin.site.register(Us)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'cteated_time', 'modified_time', 'category', 'tag_name')
    # fields = ['title', 'content', 'modified_time', 'tags']
    # 新增界面
    # fieldsets = (
    #     ('标题/正文', {'fields': ['title']}),
    # )
    # 搜索框
    search_fields = [
        'title',
    ]
    # 过滤器
    list_filter = [
        'title'
    ]

