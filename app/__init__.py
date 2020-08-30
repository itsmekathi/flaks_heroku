from flask import Flask
import click
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from flask_toastr import Toastr
from datetime import datetime
from flask_moment import Moment
from flask_pagedown import PageDown

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
toastr = Toastr()
moment = Moment()
pagedown = PageDown()


login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to continue'
login_manager.login_message_category = "info"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    toastr.init_app(app)
    moment.init_app(app)
    pagedown = PageDown(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/user')

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint, url_prefix='/post')

    from app.todolists import todolists as todolists_blueprint
    app.register_blueprint(todolists_blueprint, url_prefix='/todolists')

    from app.contacts import contacts as contacts_blueprint
    app.register_blueprint(contacts_blueprint, url_prefix='/contacts')

    from app.expenses import expenses as expenses_blueprint
    app.register_blueprint(expenses_blueprint, url_prefix='/expenses')

    from app.inventory import inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    from app.bookmarks import bookmarks as bookmarks_blueprint
    app.register_blueprint(bookmarks_blueprint, url_prefix='/bookmarks')

    from app.lists import lists as lists_blueprint
    app.register_blueprint(lists_blueprint, url_prefix='/lists')

    from app.journal import journal as journal_blueprint
    app.register_blueprint(journal_blueprint, url_prefix='/journal')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    @app.context_processor
    def inject_environment_variables():
        return dict(environment=config_name)

    @app.context_processor
    def inject_configuration():
        return dict(config=config[config_name])

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.context_processor
    def utility_processor():
        def square_number(number):
            return number * number
        return dict(square_number=square_number)

    return app
