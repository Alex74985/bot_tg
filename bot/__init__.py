from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from threading import Thread
from . models import session


babel = Babel()
migrate = Migrate()
bcrypt = Bcrypt()
db = session


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    babel.init_app(app)
    # bcrypt.init_app(app)
    # migrate.init_app(app, db, render_as_batch=True)

    from bot.routes import MyMainView
    from bot.models import Data, Draw, DrawPlayer
    from .views.draw_view import DrawView
    from .views.token_view import TokenView
    from .views.player_view import PlayerView
    admin = Admin(app, 'Admin', template_mode='bootstrap4', url='/', index_view=MyMainView())

    admin.add_view(TokenView(Data, db, name='token бота'))
    admin.add_view(DrawView(Draw, db, name='Розыгрыши'))
    admin.add_view(PlayerView(DrawPlayer, db, name='Участники'))

    return app

