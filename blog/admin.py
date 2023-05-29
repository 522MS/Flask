from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blog import models
from blog.models.database import db
from flask import redirect, url_for
from flask_login import current_user


class CustomView(ModelView):
    def create_blueprint(self, admin):
        blueprint = super().create_blueprint(admin)
        blueprint.name = f'{blueprint.name}_admin'
        return blueprint

    def get_url(self, endpoint, **kwargs):
        if not (endpoint.startswith('.') or endpoint.startswith('admin.')):
            endpoint = endpoint.replace('.', '_admin.')
        return super().get_url(endpoint, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin = Admin(name="Blog Admin", template_mode="bootstrap4")


class TagAdminView(CustomView):
    column_searchable_list = ("name",)
    column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))


class UserAdminView(CustomView):
    column_exclude_list = ("_password",)
    column_searchable_list = ("first_name", "last_name", "username", "is_staff", "email")
    column_filters = ("first_name", "last_name", "username", "is_staff", "email")
    column_editable_list = ("first_name", "last_name", "is_staff")
    can_create = True
    can_edit = True
    can_delete = False


admin.add_view(UserAdminView(models.User, db.session, category="Models"))
