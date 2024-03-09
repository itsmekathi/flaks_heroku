"""Initialize any app extensions."""

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_toastr import Toastr
from flask_moment import Moment

scheduler = APScheduler()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
toastr = Toastr()
moment = Moment()