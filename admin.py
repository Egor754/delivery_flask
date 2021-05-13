from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from models import User, Orders, db, Food, Category


class ModelUser(ModelView):
    def is_accessible(self):
        return current_user.is_admin


admin = Admin(name='Delivery', template_mode='bootstrap3')
admin.add_view(ModelUser(User, db.session))
admin.add_view(ModelUser(Orders, db.session))
admin.add_view(ModelUser(Food, db.session))
admin.add_view(ModelUser(Category, db.session))
