from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message = 'info'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main import main as main_blueprint
    from app.users import users as users_blueprint
    from app.posts import posts as posts_blueprint
    from app.todolists import todolists as todolists_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(todolists_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    

    @app.context_processor
    def inject_environment_variables():
        return dict(environment=config_name) 
        
    @app.context_processor
    def utility_processor():
        def square_number(number):
            return number * number
        return dict(square_number=square_number)

    return app
