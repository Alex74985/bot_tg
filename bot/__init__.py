from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from threading import Thread


db = SQLAlchemy()
babel = Babel()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    babel.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from bot.routes import MyMainView
    from bot.models import Winners, Data, Draw, DrawPlayer
    admin = Admin(app, 'Admin', template_mode='bootstrap4', url='/', index_view=MyMainView())

    admin.add_view(ModelView(Data, db.session))
    admin.add_view(ModelView(Winners, db.session))
    admin.add_view(ModelView(Draw, db.session))
    admin.add_view(ModelView(DrawPlayer, db.session))

    return app

