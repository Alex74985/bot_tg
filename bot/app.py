import telebot
from fsm import FSM
from base import DataBase
from models import Data
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

bot_base = DataBase()
BOT_TOKEN = bot_base.get_one(Data).bot_id

bot = telebot.TeleBot(BOT_TOKEN)
fsm_base = DataBase()
middleware_base = DataBase()
main_base = DataBase()
tool_base = DataBase()
post_base = DataBase()
end_base = DataBase()
fsm = FSM(fsm_base)
