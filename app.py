import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from models.auth import Role, User
from extentions import db, admin
from admin.model_view import AuthModelView
from home.views import home as home_blueprint
from facilitator.views import facilitator as faci_blueprint
from forms.security_forms import ExtenedLoginForm

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# init extentions
db.init_app(app)

# register blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(faci_blueprint, url_prefix=app.config['FACILITATOR_PREFIX'])

admin.init_app(app)
# Add model views
admin.add_view(AuthModelView(Role, db.session))
admin.add_view(AuthModelView(User, db.session))

with app.app_context():
    db.create_all()


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtenedLoginForm)

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


# define a context processor for merging flask-admin's template context into the
# flask-security views.
def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    with app.app_context():
        db.drop_all()
        db.create_all()
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', ' ', 'Stacey', 'Lucy'
        ]

        for i in range(len(names)):
            tmp_email = names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                name=names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True, port=8200)
