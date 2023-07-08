from earth.settings import EMAIL_TO, EMAIL_CC, EMAIL_INFO,logger
import yagmail
import traceback
def send_email(subject, content, attrs=None, to=EMAIL_TO, cc=EMAIL_CC):
    '''
    :param subject:标题
    :param content: 内容
    :param attrs: 附件，多个传list
    :param to: 发送给谁
    :param cc: 抄送
    :return:
    '''
    try:
        smtp = yagmail.SMTP(**EMAIL_INFO)
        smtp.send(to=to, contents=content, subject=subject, attachments=attrs, cc=cc)
    except :
        logger.exception("发送邮件出错："+traceback.format_exc())


