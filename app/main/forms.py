# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask.ext.pagedown.fields import PageDownField


class EditProfileForm(Form):
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'提交')


class PostForm(Form):
    body = PageDownField(u'写博客？', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class CommentForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField(u'提交')