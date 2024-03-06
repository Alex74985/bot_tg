from flask import url_for, redirect
from flask_admin import expose, BaseView, AdminIndexView
from sqlalchemy import desc


from bot.models import Draw


class MyMainView(AdminIndexView):
    @expose('/')
    def admin_main(self):
        return self.render('./base.html')
