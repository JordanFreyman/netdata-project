"""Initialize Flask-Admin and configure admin access restrictions."""

from flask import redirect, url_for
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from .models import db, User


class SecureAdminIndexView(AdminIndexView):
    """Custom Admin index view restricted to Admin users."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


class SecureModelView(ModelView):
    """Secure model view restricted to Admin users."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


def init_admin(app):
    """Initialize the Flask-Admin interface."""
    admin = Admin(
        app,
        name='Admin Panel',
        template_mode='bootstrap3',
        index_view=SecureAdminIndexView()
    )
    admin.add_view(SecureModelView(User, db.session))
