# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_security import login_required

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html')

@home.route('/login')
def login():
    return 'login'