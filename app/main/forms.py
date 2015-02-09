# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditProfileForm(Form):
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介绍')
    submit = SubmitField(u'提交')


class PostForm(Form):
    body = TextAreaField(u'有什么要说的？', validators=[DataRequired()])
    submit = SubmitField(u'提交')