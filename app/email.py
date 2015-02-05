# -*- coding: utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():  # 激活上下文
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    # msg = Message('test subject', sender='leonhanxl@163.com',
    #              recipients=['985229518@qq.com'])
    # msg.body = 'text body'
    # msg.html = '<b>HTML</b> body'
    # with current_app.app_context():
    #     mail.send(msg)