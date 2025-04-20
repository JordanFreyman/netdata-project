from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from .models import db, User

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

def init_admin(app):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=SecureAdminIndexView())
    admin.add_view(SecureModelView(User, db.session))
