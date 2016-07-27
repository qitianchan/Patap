# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for
from flask_security import login_required, current_user, roles_accepted

facilitator = Blueprint('facilitator', __name__)


@facilitator.route('/')
@login_required
def dashboard():
    if 'superuser' in [role.name for role in current_user.roles]:
        return redirect(url_for('admin.index'))
    return 'dashboard'
