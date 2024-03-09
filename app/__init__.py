from flask import Flask
from config import config
from datetime import datetime
from .extensions import scheduler, db, login_manager, bcrypt, mail, toastr, moment

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

    # Initialize scheduler
    scheduler.init_app(app)
    from . import jobs
    scheduler.start()

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

    from app.timezone import timezone as timezone_blueprint
    app.register_blueprint(timezone_blueprint, url_prefix="/timezone")

    ## from app.journal import journal as journal_blueprint
    ## app.register_blueprint(journal_blueprint, url_prefix='/journal')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    from .health import health as health_blueprint
    app.register_blueprint(health_blueprint, url_prefix="/health")

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
