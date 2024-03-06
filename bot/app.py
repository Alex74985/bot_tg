import telebot
from base import DataBase
from fsm import FSM
import models
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# app = Flask(__name__)
#
#
# class MyView(ModelView):
#     excluded_list_columns = ('message_id', 'file_type', 'file_id', 'chanel_name', )
#
#     # @expose('/')
#     # def index(self):
#     #     return self.render('./base.html')
#
#
# admin = Admin(app)
# admin.add_view(MyView(models.Draw, models.session, name='Розыгрыши'))


bot = telebot.TeleBot('7131855484:AAFoKXk28dpYmT-CCzi_xUv3887cRIqcu4U')
fsm_base = DataBase()
middleware_base = DataBase()
main_base = DataBase()
tool_base = DataBase()
post_base = DataBase()
end_base = DataBase()
fsm = FSM(fsm_base)
