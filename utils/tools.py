import datetime
import hashlib
from itertools import chain


class ExtendForm:
    # 格式化form返回的错误,这是自己扩展的类，用的form的时候，继承
    ignore_error_keys = [] #这个是存一些出错时忽略的参数名，给修改数据的时候用的，因为修改的时候，不是每个字段都要传的，这里只存传了并且校验没有通过的参数名

    @property
    def error_format(self):
        '''默认form返回的错误信息是一个字典套list，这个函数的作用是把它返回的错误信息，都拼成一个字符串'''
        error_message = ''
        for field, error_list in self.errors.get_json_data().items():
            if field not in self.ignore_error_keys:
                error_message += field + error_list[0].get('message')
        return error_message


def md5(s):
    '''md5'''
    m = hashlib.md5(s.encode())
    return m.hexdigest()


def model_to_dict(instance, fields=None, exclude=None):  # 这个函数是我新加的
    """
    fields是返回哪些字段，exclude是排除哪些字段
    这个方法是参考了django自带的model_to_dict方法，做了修改，因为django自带的model转字典的方法
    日期类型的它不返回，所以改了一下，源码的位置在
    from django.forms.models import model_to_dict
    """
    opts = instance._meta  # 所有的字段
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields and f.name not in fields:  # 判断传进来的字段是否在表里
            continue
        if exclude and f.name in exclude:  # 判断是否有排除的字段
            continue
        value = f.value_from_object(instance)
        if isinstance(value, datetime.datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        data[f.name] = value
    return data
