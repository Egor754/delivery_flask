from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import User, Orders, db, Food, Category

admin = Admin()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Orders, db.session))
admin.add_view(ModelView(Food, db.session))
admin.add_view(ModelView(Category, db.session))
