from celery import Celery
app = Celery('sksystem')

# 获取celery的配置信息
app.config_from_object('celery_tasks.config')
# 提供tasks的路径，自动发现需要运行的task任务
app.autodiscover_tasks(['celery_tasks.run'])

# 启动celery的方法 默认以cpu的核数多进程的方式启动
# celery -A 应用路径 worker -l 日志级别
# mac同学
# celery -A celery_tasks.main worker -l info 普通启动
# celery multi start w1 -A celery_tasks.main -l info  --logfile=logs/celerylog.log --pidfile=logs/celerypid.pid 后台运行
# celery flower -A celery_tasks.main 打开一个web页面启动 需要提前安装下flow  安装命令：pip install flower

# win同学

# -- * - **** ---
# - ** ---------- [config]
# - ** ---------- .> app:         sksystem:0x103d0deb8                      启动是那个app的任务
# - ** ---------- .> transport:   redis://10.168.100.21:6379/2              设置的broker的队列是那个
# - ** ---------- .> results:     redis://10.168.100.21:6379/3              设置backend的存储地址
# - *** --- * --- .> concurrency: 4 (prefork)                               默认启动的进程数
# -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
# --- ***** -----
#  -------------- [queues]
#                 .> celery           exchange=celery(direct) key=celery


# 在view视图中只需要导入tasks中写好的任务方法 通过任务方法调用delay()即可
# from celery_tasks.run.tasks import run_case
# 调用task任务 参数可以在delay中传递，正常调用一样
# run_case.delay()
