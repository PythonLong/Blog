from flask_mail import Message
from app import mail
from flask import render_template,current_app
from threading import Thread




#异步发送邮件


def send_async_eamil(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(subject,recipients=[to])

    #渲染 需要的参数 通过**kwagrs传入
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)

    thr = Thread(target=send_async_eamil,args=[app,msg])
    thr.run()
    return thr



