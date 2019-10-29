from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255, collation='NOCASE'),
                      nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'),
                           nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'),
                          nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    # Define the posts related to the user
    posts = db.relationship('Post', backref='author', lazy=True)

    # Define the todolists for the user
    todoLists = db.relationship('ToDoList', backref="user", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))

# Define the Post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class ToDoList(db.Model):
    __tablename__='todo_lists'
    id = db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    todo_items = db.relationship('ToDoItem', backref='todolist', lazy=True)
    date_created = db.Column(db.DateTime(), nullable=False, default = datetime.utcnow)
    date_modified = db.Column(db.DateTime(), nullable=False, default= datetime.utcnow)

class TaskStatusLu(db.Model):
    __tablename__ = "task_status_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(db.String(200), nullable=False, default="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_status') 


class TaskPriorityLu(db.Model):
    __tablename__="task_priority_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(db.String(200), nullable=False, default ="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_priority') 

class TaskUrgencyLu(db.Model):
    __tablename__ = "task_urgency_lu"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(db.String(200), nullable=False, default="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_urgency') 
    
class ToDoItem(db.Model):
    __tablename__="todo_items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(200), nullable=False)
    status_id = db.Column(db.Integer(), db.ForeignKey('task_status_lu.id'), nullable=False)
    priority_id = db.Column(db.Integer(), db.ForeignKey('task_priority_lu.id'), nullable=False )
    urgency_id = db.Column(db.Integer(), db.ForeignKey('task_urgency_lu.id'), nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)
    scheduled_date = db.Column(db.DateTime(), nullable=False, default = datetime.utcnow)
    estimated_duration_hours = db.Column(db.Integer(), nullable=False, default=0)
    estimated_duration_minutes = db.Column(db.Integer(), nullable=False, default = 0)
    actual_duration_hours = db.Column(db.Integer(), nullable=False, default = 0)
    actual_duration_minutes = db.Column(db.Integer(), nullable=False, default = 0)
    comments = db.relationship('ToDoItemComments', backref='todoitem') 
    date_created = db.Column(db.DateTime(), nullable=False, default = datetime.utcnow)
    date_modified = db.Column(db.DateTime(), nullable=False, default= datetime.utcnow)

class ToDoItemComments(db.Model):
    __tablename__="todo_items_comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300), nullable=False)
    todo_item_id = db.Column(db.Integer(), db.ForeignKey('todo_items.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    comment_date = db.Column(db.DateTime(), nullable=False, default= datetime.utcnow)