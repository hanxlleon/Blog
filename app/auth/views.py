# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     # form = NameForm()
#     if form.validate_on_submit():
#         return redirect(url_for('.index'))
#     return render_template('index.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)  # 是否记录登录状态
            # request.args.get('next')会记录上次的页面
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误！')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash(u'你现在可以登录了！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

