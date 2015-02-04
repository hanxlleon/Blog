# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import login_user
from . import main
from .forms import LoginForm
from .. import db
from ..models import User


# @main.route('/', methods=['GET', 'POST'])
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user, form.remember_me.data)  # 是否记录登录状态
#             # request.args.get('next')会记录上次的页面
#             return redirect(request.args.get('next') or url_for('main.index'))
#         flash(u'用户名或密码错误！')
#     return render_template('main/login.html', form=form)
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')