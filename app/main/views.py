# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, abort, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm
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


@main.route('/user/<username>')
def user(username):
    usr = User.query.filter_by(username=username).first()
    if usr is None:
        abort(404)
    return render_template('user.html', user=usr)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的用户资料已经更新！')
        return redirect(url_for('.user', username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)