# -*- coding: utf-8 -*-
from flask_security.forms import LoginForm
from wtforms import StringField, PasswordField, validators, \
    SubmitField, HiddenField, BooleanField, ValidationError, Field
_default_field_labels = {
    'email': '电子邮箱',
    'password': '密码',
    'remember_me': '记住我',
    'login': '登录',
    'retype_password': '重新输入密码',
    'register': '注册',
    'send_confirmation': 'Resend Confirmation Instructions',
    'recover_password': 'Recover Password',
    'reset_password': '重置密码',
    'new_password': '新密码',
    'change_password': '改变密码',
    'send_login_link': '发送登录链接'
}

def get_form_field_label(key):
    return _default_field_labels.get(key, '')


class ExtenedLoginForm(LoginForm):
    email = StringField(get_form_field_label('email'))
    password = PasswordField(get_form_field_label('password'))
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))