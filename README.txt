# skbackend

#### 介绍
django服务端开发，base工程

#### 安装教程

1.  安装 requirements.txt中的依赖软件即可,pip install -r requirements.txt
2.  安装完成后，运行start_server.py即可启动，默认端口号是8999，自己可以在start_server中修改
    或者使用django自带的runserver命令也可以
3.  admin账号密码：admin/123456

#### 使用说明

1.  example是例子，按照例子写即可，里面有个登录例子的view，需要用到redis，如果用的话，要在setting中提前配置好
2.  写自己的系统，重新创建一个app，加入到setting里面即可 （startapp）
3.  请求例子：
        1.  获取数据，get请求
            1.  http://127.0.0.1:8999/example/book/?limit=20&page=1     get请求获取数据，默认limit和page可以不写，不写的话，默认每页20，取第一页
            2.  http://127.0.0.1:8999/example/book/?search=倚天           模糊查询，传search参数即可，分页和上面一样
            3.  http://127.0.0.1:8999/example/book/?price=51&count=5    条件筛选，传对应的参数即可,在view里面配置的，分页和上面一样
        2.  新增数据，post请求
           http://127.0.0.1:8999/example/book  #写好参数传就ok了
                name = xxx
                price = 98.1
                count = 99
                author = 1
        3.  修改数据，put请求
                http://127.0.0.1:8999/example/book?id=5 #url里面传入id，然后修改什么字段，在body里面传就ok了
                    name = 雪山飞狐
        4.  删除，delete请求
                http://127.0.0.1:8999/example/book?id=5 #url里面传入id
                
        

