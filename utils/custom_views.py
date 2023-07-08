import copy
from django.core.paginator import Paginator
from django.db.models import Q, Model
from django.views import View
from .custom_response import NbResponse
from . import const
from utils.tools import model_to_dict
from django.forms import BaseForm


class BaseView(View):
    search_field = []  # 根据哪些字段来搜索
    filter_field = []  # 根据哪些字段来搜索
    model_class = None  # 用哪个model类
    form_class = None  # 用哪个form类
    exclude_fields = ['is_delete']  # 返回的时候排除哪些字段
    fields = []  # 返回的时候显示哪些字段，空list就是所有的字段

    @property
    def query_set(self):
        '''获取某个数据的实例，返回的是一条数据的query_set，query_set有 update方法'''
        id = self.request.GET.get('id', 0)
        query_set = self.model.objects.filter(pk=id)
        if query_set:
            return query_set

    @property
    def model_instance(self):
        '''获取某个数据的实例，返回的是一条数据的对象，他没有update方法'''
        if self.query_set:
            return self.query_set.first()

    def delete_model(self):
        '''逻辑删除数据'''
        if self.model_instance:
            fields = self.model_instance._meta.fields
            # 逻辑删除时，同时修改所有唯一字段的值 在值的后面增加 当前字段的主键ID
            uniques = {}
            for field in fields:
                if field.unique and field.name != 'id':
                    uniques[field.name] = getattr(self.model_instance, field.name) + '_del_' + str(self.model_instance.id)
            uniques['is_delete'] = 0
            self.query_set.update(**uniques)  # 逻辑删除
            return True
        return False

    def get_filter_dict(self):
        '''获取过滤的数据'''
        filter_dict = {}  # 这个是用来过滤数据的字典 {'id':1,'name':'abc','phone':xxx} id=1,name=abc,phone=xxx
        for field in self.filter_field:  # 循环获取到有哪些过滤的字段
            value = self.request.GET.get(field)
            if value:
                filter_dict[field] = value
        return filter_dict

    def get_search_obj(self):
        '''获取模糊查询的'''
        q_result = Q()  # 保存模糊查询的对象
        search = self.request.GET.get('search')
        if search:
            for field in self.search_field:
                d = {'%s__contains' % field: search}  # {name__contains:abc}
                q_result = Q(**d) | q_result
        return q_result

    @property
    def form(self):
        '''获取form_class'''
        if self.form_class and issubclass(self.form_class, BaseForm):  # 判断如果没有实现，或者指定的类不对，直接抛出异常
            return self.form_class
        raise Exception('请指定form类')

    @property
    def model(self):
        if self.model_class and issubclass(self.model_class, Model):  # 判断如果没有指定model类，或者指定的类型不对，就报错
            return self.model_class
        raise Exception("请指定model类")

    def paginator(self, obj_list):
        '''分页'''
        try:
            limit = int(self.request.GET.get('limit', const.page_limit))
            page = int(self.request.GET.get('page', 1))
        except:
            limit = const.page_limit
            page = 1
        page_obj = Paginator(obj_list, limit)
        result = list(page_obj.get_page(page))
        return result, page_obj

    def get_fs_query_set(self):
        '''获取经过筛选和模糊查询之后的query_set对象'''
        filter_dict = self.get_filter_dict()
        q_result = self.get_search_obj()
        query_set = self.model.objects.filter(is_delete=1).filter(**filter_dict).filter(q_result)  # 获取到查询的query_set
        return query_set

    def get_query_set_page_data(self):
        '''获取query_set分页之后的数据'''
        query_set = self.get_fs_query_set()  # 获取查询数据
        page_data, page_obj = self.paginator(query_set)  # 分页
        return page_data, page_obj


class GetView:
    def get(self, request):
        page_data, page_obj = self.get_query_set_page_data()  # 获取分页之后的数据
        data_list = []
        for instance in page_data:  #
            model_dict = model_to_dict(instance, self.fields, self.exclude_fields)  # 转成字典
            data_list.append(model_dict)
        return NbResponse(data=data_list, count=page_obj.count)


class PostView:

    def post(self, request):
        form_obj = self.form(request.POST,request.FILES)
        if form_obj.is_valid():
            self.model.objects.create(**form_obj.cleaned_data)
            ret = NbResponse()  # 默认请求成功
        else:
            ret = NbResponse(code=-1, msg=form_obj.error_format)
        return ret


class DeleteView:
    def delete(self, request):
        if self.delete_model():
            return NbResponse()
        return NbResponse(404, 'id不存在')


class PutView:
    # def get_error_keys(self):
    #     error_keys = set(self.form_obj.errors.get_json_data().keys())  # 校验没有通过的字段
    #     put_keys = set(self.request.PUT.keys())  # 传过来的字段
    #     input_error_key = list(error_keys & put_keys)  # 取传入字段和错误字段的交集
    #     after_unique_key = self.check_unique_field(input_error_key)  # 校验唯一的字段是否和现在的数据一样，如果一样就删除key
    #     self.form_obj.ignore_error_keys = set(self.form_obj.fields) - put_keys
    #     # 取差集，这里是因为如果传过来的字段有错误的话，他会把那些新增时候必传的字段也放在错误里
    #     # 把所有的字段和传过来要修改的字段取一下差集，获取不修改的字段，把他们的错误信息忽略了就ok了
    #     # 在error_format里面取错误信息的时候判断了
    #     return after_unique_key

    # def check_unique_field(self, error_keys):
    #     if not error_keys:  # 如果是空，直接返回
    #         return error_keys
    #     error_keys_copy = copy.copy(error_keys)
    #     for key in error_keys:
    #         field = self.instance.first()._meta.get_field(key)  # 获取字段的类型
    #         if field.unique and self.request.PUT.get(key) == str(getattr(self.instance.first(), key)):
    #             # 判断如果字段类型是唯一的，并且这两个是传过来的数据是一样的就把这个参数删除
    #             error_keys_copy.remove(key)
    #     return error_keys_copy

    # def put(self, request):  # 修改
    #     if not self.query_set:  # 如果查出来数据为空
    #         return NbResponse(code=404, msg='id不存在')
    #     self.form_obj = self.form(request.PUT)  # 它校验的是全部的字段
    #     clean_data = {}
    #     if self.form_obj.is_valid():
    #         clean_data = self.form_obj.cleaned_data
    #     elif self.get_error_keys():  # 获取有没有错误的key
    #         return NbResponse(code=-1, msg=self.form_obj.error_format)
    #     else:  # 没有交集说明穿过的字段都通过了校验
    #         for k in request.PUT.keys():
    #             clean_data[k] = request.PUT.get(k)
    #     self.query_set.update(**clean_data)
    #     return NbResponse()

    def put(self,request):
        form = self.form(request.PUT,files=request.FILES,instance=self.model_instance)
        if form.is_valid():
            form.save()
            return NbResponse()
        return NbResponse(401,msg=self.error_format)


class NbView(BaseView, GetView, PostView, DeleteView, PutView):
    '''继承了这个类，就自动实现了增删改查所有的'''
    pass
