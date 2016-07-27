# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
db = SQLAlchemy()
admin = Admin(name='Patap',
              base_template='admin_base.html',
              template_mode='bootstrap3',
              )

