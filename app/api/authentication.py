from flask_httpauth import HTTPBasicAuth
from app.models import User
from app import bcrypt, db
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email = email).first()
    if not User:
        return False
    g.current_user = user
    return bcrypt.check_password_hash(user.password, password)

@auth.error_handler
def auth_error():
    return unau