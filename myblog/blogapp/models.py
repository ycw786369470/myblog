'''
    一、
        0、早期个人博客√
        1、登录、注册界面√
        2、登陆成功后直接跳转至博客主页，左上角“登录”更改为欢迎xxx√
        3、登陆后才能发表博客文章，游客禁止√
        4、发布文章界面完善√
        5、点赞系统完善√
        6、游客禁止点赞界面√
        7、个人界面√
        8、餐厅功能(目前账号密码与博客共享)
    二、每次迁移数据后应该做什么？
        0、shell中新增tag表
            'E:\work\python\学习笔记\django.docx'末尾
        1、新增超级用户
            python manage.py createsuperuser
        2、创建博客管理员用户
        3、新增餐厅信息
        4、给餐厅新增菜单
        ...
'''

from DjangoUeditor.models import UEditorField
from django.db import models
from myblog import settings
from PIL import Image
# from django.db.
import os
from django import forms


# Create your models here.
class DjangoForm(forms.Form):
    content = UEditorField(
        '内容', width=600, height=300, toolbars="full", imagePath="ueditor/",
        filePath="ueditor/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}
    )


class NewForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

    # 内置类修改名字
    class Meta:
        verbose_name_plural = '分类'


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = '标签'


class Post(models.Model):
    """博客文章类"""
    title = models.CharField('标题', max_length=100)    # 标题
    content = models.CharField('内容', max_length=100)  # 内容
    # 分类
    category = models.ForeignKey(Category)
    # 标签
    tags = models.ManyToManyField(Tag, blank=True)  # 是否允许为空
    delete = models.BooleanField(default=False)
    # 创建时间
    cteated_time = models.DateTimeField('创建时间')
    # 发布时间
    modified_time = models.DateTimeField('发布时间')

    def tag_name(self):
        return ''.join([str(i) for i in self.tags.all()])

    class Meta:
        verbose_name_plural = '博客'


class Users(models.Model):
    photo = models.ImageField(upload_to='blog/', blank=True)
    thumb = models.ImageField(upload_to='thumb/', blank=True)   # 缩略图
    name = models.CharField(max_length=25)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    gender = models.BooleanField(default=True)
    habits = models.ForeignKey(Tag)
    is_boss = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(Users, self).save()   # 调用父类方法
    #     # 获取上传的文件名称以及后缀
    #     img_name, ext = os.path.splitext(os.path.basename(self.photo.name))
    #     # 获取上传的大图路径
    #     img_path = os.path.join(settings.THUMB_DIR, self.photo.name)
    #     # 生成缩略图
    #     pix = make_thumb(img_path)
    #     # 保存缩略图到配置路径下
    #     thumb_path = os.path.join(settings.THUMB_DIR, img_name,)
    #     # 将索罗图的url保存到数据库


class BlogUser(models.Model):
    name = models.ForeignKey(Users)
    title = models.CharField(max_length=30)
    content = UEditorField(width=1000, height=300, toolbars="full", imagePath="", filePath="")
    time = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag)
    visit = models.IntegerField(default=0)

    def __str__(self):
        return self.name.name

    @classmethod
    def add_user(cls, name, content, time):
        self = cls(name=name, content=content, time=time)
        return self

    class Meta:
        verbose_name_plural = '全部博客'


class Comment(models.Model):
    name = models.ForeignKey(Users)          # 评论用户
    content = models.TextField()                # 内容
    time = models.DateTimeField()               # 发表评论时间
    user = models.ForeignKey(BlogUser)      # 评论文章，一对多

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '评论'


# 点赞数
class Mark(models.Model):
    # 点赞用户
    mark_name = models.ForeignKey(Users)
    # 点赞数
    up_num = models.IntegerField(default=0)
    # 踩数
    down_num = models.IntegerField(default=0)
    # 收藏数
    star_num = models.IntegerField(default=0)
    # 被点赞用户
    name = models.ForeignKey(BlogUser)

    def __str__(self):
        return str(self.name)


class UserUp(models.Model):
    # 被mark的文章
    name = models.ForeignKey(BlogUser)
    # mark用户
    mark_name = models.ForeignKey(Users)
    # 是否点过赞？默认为False
    is_over = models.BooleanField(default=False)


class UserDown(models.Model):
    name = models.ForeignKey(BlogUser)
    mark_name = models.ForeignKey(Users)
    is_over = models.BooleanField(default=False)


class UserStar(models.Model):
    name = models.ForeignKey(BlogUser)
    mark_name = models.ForeignKey(Users)
    is_over = models.BooleanField(default=False)


# 上传图片
class Upload(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.name


# 新博客项目模型类
# 每日一句
class Sentence(models.Model):
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '每日一句'


# 文章
class NewBlog(models.Model):
    title = models.CharField(max_length=50)
    choices = (
        ('网站前端', '网站前端'),
        ('后端技术', '后端技术')
    )
    classfy = models.CharField('分类', max_length=20, choices=choices)
    source = models.CharField('来源', max_length=50)
    look = models.IntegerField('围观次数', default=0)
    content = UEditorField(width=1000, height=300, toolbars="full", imagePath="", filePath="")
    pub_time = models.DateTimeField('发布时间', auto_now_add=True)
    mod_time = models.DateTimeField('修改时间', auto_now=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Users)

    img = models.ImageField()
    adv = models.BooleanField('是否为广告位推广', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'


# 留言
class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '留言'


# 友情链接
class FriendLink(models.Model):
    web_img = models.ImageField(upload_to='blog/')
    web_name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    introduce = models.CharField(max_length=1000)

    def __str__(self):
        return self.web_name

    class Meta:
        verbose_name_plural = '友情链接'


# 关于我们
class Us(models.Model):
    QQ = models.CharField(max_length=15)
    QQgroup = models.CharField(max_length=15)
    content = models.CharField(max_length=1000)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '关于我们'


# 餐厅模型部分
class Canteen(models.Model):
    canteen_name = models.CharField(max_length=50)
    canteen_boss = models.CharField(max_length=30)
    canteen_num = models.CharField(max_length=10)       # 餐厅编号

    def __str__(self):
        return self.canteen_name


# 餐厅餐桌表
class Table(models.Model):
    canteen = models.ForeignKey(Canteen)
    table_num = models.IntegerField(default=8)
    table_clients = models.IntegerField(default=0)
    table_food = models.CharField(max_length=300, default='none')
    is_over = models.BooleanField(default=False)

    def __str__(self):
        return self.canteen.canteen_name + 'self.id'


class Menu(models.Model):
    canteen = models.ForeignKey(Canteen)
    food_name = models.CharField(max_length=30, default='暂无')
    food_img = models.ImageField(upload_to='canteen/img/', blank=True)
    food_price = models.FloatField(default=0)       # 价格
    food_intro = models.CharField(max_length=200)   # 简介
    food_num = models.IntegerField(default=0)       # 菜品库存
    food_up = models.IntegerField(default=0)        # 菜品点赞量
    food_sold = models.IntegerField(default=0)      # 历史售量

    def __str__(self):
        return self.food_name

    @classmethod
    def add_food(cls, canteen,
                 food_name, food_img,
                 food_price, food_intro,
                 food_num, food_up,
                 food_sold):
        self = cls(canteen=canteen, food_name=food_name,
                   food_img=food_img, food_price=food_price,
                   food_intro=food_intro, food_num=food_num,
                   food_up=food_up, food_sold=food_sold)
        return self

    class Meta:
        verbose_name_plural = '菜单'


# 客户消费记录
class ClientHistory(models.Model):
    client = models.ForeignKey(Users)
    canteen = models.ForeignKey(Canteen)
    client_num = models.IntegerField(default=1)                     # 用餐人数
    table = models.IntegerField(default=0)
    consume_time = models.DateTimeField(auto_now_add=True)          # 消费时间
    food = models.CharField(max_length=800)                         # 菜单记录
    price = models.FloatField()                                     # 价格
    paid = models.BooleanField(default=False)                       # 是否支付


def make_thumb(img_path, size=(80, 80)):
    '''
        制作缩略图
        img_path：图片路径
        size：缩略图尺寸
        return：返回缩咯图
    '''
    img = Image.open(img_path)  # 打开图片
    img.thumbnail(size)         # 压缩成指定尺寸
    return img






