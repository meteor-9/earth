import time, django_redis,pickle
from django.views import View
from utils.custom_views import NbView, BaseView, PostView, GetView
from utils.tools import model_to_dict
from . import models, forms
from utils import const
from utils.custom_response import NbResponse
from utils.tools import md5

class AuthorView(NbView):
    search_field = ['name']  # 搜索的时候根据哪些字段搜
    filter_field = ['id', 'name']  # 过虑的时候根据哪些字段过虑
    model = models.Author  # model类
    form_class = forms.AuthorForm  # form类


class BookView(NbView):
    search_field = ['name']
    filter_field = ['id', 'name', 'author_id']
    model_class = models.Book
    form_class = forms.BookForm


class BookAddView(BaseView, PostView):
    '''继承了这2个类，就只有新增的功能'''
    search_field = ['name']
    filter_field = ['id', 'name', 'author_id']
    model_class = models.Book
    form_class = forms.BookForm


class BookQueryAddView(BaseView, GetView, PostView):
    '''继承了这3个类，就只有新增和查询的功能'''
    search_field = ['name']
    filter_field = ['id', 'name', 'author_id']
    model_class = models.Book
    form_class = forms.BookForm


class BookV2(NbView):
    '''这个类是为了说明自己加字段的时候怎么搞'''
    search_field = ['name']
    filter_field = ['id', 'name', 'author']
    model_class = models.Book
    form_class = forms.BookForm

    def get(self, request):
        page_data, page_obj = self.get_query_set_page_data()  # 获取分页之后的数据
        data_list = []
        for instance in page_data:
            model_dict = model_to_dict(instance, self.fields, self.exclude_fields)  # 转成字典
            model_dict['author_name'] = instance.author.name  # 给字典里面加字段
            data_list.append(model_dict)
        return NbResponse(data=data_list, count=page_obj.count)


class LoginView(View):
    '''登录'''
    def post(self, request):
        user_form_obj = forms.LoginForm(request.POST)
        if user_form_obj.is_valid():
            #因为forms里面在clean里头写过校验账号密码了，所以这里不用写了
            user = user_form_obj.cleaned_data['user']
            token = '%s%s' % (user.phone, time.time())
            token = md5(token)
            try:
                redis = django_redis.get_redis_connection()
            except:
                raise Exception("连接不上redis，请检查redis！")
            redis.set(const.token_prefix+token, pickle.dumps(user), const.token_expire)
            return NbResponse(token=token, user=user.username)
        else:
            return NbResponse(-1, user_form_obj.error_format)


class LogoutView(View):
    '''退出'''
    def post(self, request):
        redis = django_redis.get_redis_connection()
        redis.delete(const.token_prefix+request.token)
        return NbResponse()











