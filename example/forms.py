from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, Form
from django import forms

from . import models
from utils.tools import ExtendForm


class BookForm(ModelForm, ExtendForm):
    class Meta:
        model = models.Book
        exclude = ['is_delete']  # form的时候排除哪些字段
        # fields = [] #展示哪些字段

    def clean_price(self):  # 校验price的钩子
        price = self.cleaned_data['price']
        if price <= 0:
            self.add_error('price','价格不能小于0')
        return price


class AuthorForm(ModelForm, ExtendForm):
    class Meta:
        model = models.Author
        exclude = ['is_delete']


class LoginForm(Form, ExtendForm):
    username = forms.CharField(min_length=5, max_length=20, required=True)
    password = forms.CharField(min_length=6, max_length=20, required=True)

    def clean(self):
        if not self.errors:  # 校验errors里面是否有错误
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = models.User.objects.filter(Q(phone=username) | Q(email=username))
            if user:
                user = user.first()
                if user.check_password(password):
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    self.add_error('password','密码错误')
            else:
                self.add_error('username', '用户不存在')
