from django.urls import path
from . import views
urlpatterns = [
    path('book_add/', views.BookAddView.as_view()),#只有新增
    path('book_add_query/', views.BookQueryAddView.as_view()),#新增和查询
    path('book/', views.BookView.as_view()),#增删改查都有
    path('v2/book/', views.BookV2.as_view()),#这个是自己需要自己加字段
    path('author/', views.AuthorView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]