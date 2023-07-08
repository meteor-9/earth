from django.db import models
from utils import tools
from earth import settings


class BaseModel(models.Model):
    '''公共字段'''
    is_delete_choice = (
        (0, '删除'),
        (1, '正常')
    )
    is_delete = models.SmallIntegerField(choices=is_delete_choice, default=1, verbose_name='是否被删除')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # auto_now_add的意思，插入数据的时候，自动取当前时间
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)  # 修改数据的时候，时间会自动变

    class Meta:
        abstract = True  # 只是用来继承的,不会创建这个表


class Author(BaseModel):
    name = models.CharField(verbose_name='名称', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作家'
        verbose_name_plural = verbose_name
        ordering = ['id']
        db_table = 'eg_author'


class Book(BaseModel):
    name = models.CharField(verbose_name='书名', max_length=20)
    price = models.FloatField(verbose_name='价格')
    count = models.IntegerField(verbose_name='数量')
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='作者')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        ordering = ['id']
        db_table = 'eg_book'


class User(BaseModel):
    '''用户表'''
    phone = models.CharField(verbose_name='手机号', max_length=11, unique=True)
    email = models.EmailField(verbose_name='邮箱', max_length=25, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    nick = models.CharField(verbose_name='昵称', default='Python小学生', max_length=20)

    @staticmethod
    def make_password(raw_password):
        '''生成密码'''
        before_password = '%s%s' % (raw_password, settings.SECRET_KEY)  # 生成密码的算法，可以自己改
        after_password = tools.md5(before_password)
        return after_password

    def set_password(self, raw_password):
        '''设置密码'''
        self.password = self.make_password(raw_password)

    def check_password(self, raw_password):
        '''校验登录密码'''
        return self.make_password(raw_password) == self.password

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        db_table = 'eg_user'
