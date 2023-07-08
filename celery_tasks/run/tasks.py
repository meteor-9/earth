from celery_tasks.main import app
# 在celery中使用logger
from celery.utils.log import get_task_logger
from utils.send_message import send_email
logger = get_task_logger('django_server')




@app.task(name='async_send_mail')
def async_send_mail(*args,**kwargs):
    '''异步发送邮件，调用的时候使用 async_send_mail.delay(...)'''
    send_email(*args,**kwargs)
