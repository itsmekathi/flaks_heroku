from datetime import datetime, date
from app import db, login_manager, bcrypt
from flask_login import UserMixin
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .exceptions import ValidationError


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
    email = db.Column(db.String(255),
                      nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')

    # User information
    first_name = db.Column(db.String(100),
                           nullable=False, server_default='')
    last_name = db.Column(db.String(100),
                          nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    # Define the posts related to the user
    posts = db.relationship('Post', backref='author', lazy=True)

    # Define the todolists for the user
    todoLists = db.relationship('ToDoList', backref="user", lazy=True)
    allComments = db.relationship(
        'ToDoItemComments', backref="user", lazy=True)
    workLogs = db.relationship('ToDoItemWorkLog', backref="user", lazy=True)
    contacts = db.relationship('Contact', backref="created_by", lazy=True)
    expenses = db.relationship('Expenses', backref="created_by", lazy=True)
    addresses = db.relationship('Address', backref="created_by", lazy=True)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

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

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': {'title': self.title, 'content': self.content, 'date_posted': self.date_posted, 'image_file': self.author.image_file}
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class ToDoList(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    todo_items = db.relationship(
        'ToDoItem', backref='todolist', lazy=True, cascade="save-update, merge, delete")
    date_created = db.Column(db.Date(), nullable=False, default=date.today)
    date_modified = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)

    def to_json(self):
        json_todo_list = {
            'url': url_for('api.todolists', todo_list_id=self.id),
            'body': {'id': self.id, 'title': self.title, 'description': self.description, 'create_by': self.user.username}
        }
        return json_todo_list


class TaskStatusLu(db.Model):
    __tablename__ = "task_status_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(
        db.String(200), nullable=False, default="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_status')

    def to_json(self):
        json_status = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'style_class': self.style_class
        }
        return json_status


class TaskPriorityLu(db.Model):
    __tablename__ = "task_priority_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(
        db.String(200), nullable=False, default="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_priority')

    def to_json(self):
        json_priority = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'style_class': self.style_class
        }
        return json_priority


class TaskUrgencyLu(db.Model):
    __tablename__ = "task_urgency_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    style_class = db.Column(
        db.String(200), nullable=False, default="text-danger")
    todo_items = db.relationship('ToDoItem', backref='task_urgency')

    def to_json(self):
        json_urgency = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'style_class': self.style_class
        }
        return json_urgency


class ToDoItem(db.Model):
    # -*- coding: utf-8 -*-
    """ Master table for To-Do items
    """
    __tablename__ = "todo_items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status_id = db.Column(db.Integer(), db.ForeignKey(
        'task_status_lu.id'), nullable=False)
    priority_id = db.Column(db.Integer(), db.ForeignKey(
        'task_priority_lu.id'), nullable=False)
    urgency_id = db.Column(db.Integer(), db.ForeignKey(
        'task_urgency_lu.id'), nullable=False)
    todo_list_id = db.Column(db.Integer, db.ForeignKey(
        'todo_lists.id'), nullable=False)
    scheduled_date = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    estimated_duration_hours = db.Column(
        db.Integer(), nullable=False, default=0)
    estimated_duration_minutes = db.Column(
        db.Integer(), nullable=False, default=0)
    actual_duration_hours = db.Column(db.Integer(), nullable=False, default=0)
    actual_duration_minutes = db.Column(
        db.Integer(), nullable=False, default=0)
    comments = db.relationship('ToDoItemComments', backref='todoitem',
                               lazy='select', cascade="save-update, merge, delete")
    work_logs = db.relationship('ToDoItemWorkLog', backref='todoitem',
                                lazy='select', cascade="save-update, merge, delete")
    date_created = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    date_modified = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)

    def to_json(self):
        json_todo_item = {
            'url': url_for('api.todoitems', todo_item_id=self.id),
            'body': {'id': self.id, 'title': self.title, 'description': self.description, 'status': self.task_status.name, 'priority': self.task_priority.name, 'urgency': self.task_urgency.name, 'scheduled_date': self.scheduled_date}
        }
        return json_todo_item


class ToDoItemComments(db.Model):
    __tablename__ = "todo_items_comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300), nullable=False)
    todo_item_id = db.Column(db.Integer(), db.ForeignKey(
        'todo_items.id'), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    comment_date = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)


class ToDoItemWorkLog(db.Model):
    # -*- coding: utf-8 -*-
    """ Master table for storing work log's or time
    spent on a particular task
    """
    __tablename__ = "todo_item_worklogs"
    id = db.Column(db.Integer, primary_key=True)
    todo_item_id = db.Column(db.Integer(), db.ForeignKey(
        'todo_items.id'), nullable=False)
    start_datetime = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    end_datetime = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    comment = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    date_created = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)


class ContactTypeLu(db.Model):
    # -*- coding: utf-8 -*-
    """ Master table for Contact type lookup
    Different contact types can be Store's, person, 
    """
    __tablename__ = "contact_type_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    contacts = db.relationship('Contact', backref='contact_type', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'style_class': self.style_class
        }
        return json


class Contact(db.Model):
    """ 
    Master table for Contact.
    Holds all contact information that the user is associated with
    """
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    contact_type_id = db.Column(db.Integer, db.ForeignKey(
        'contact_type_lu.id'), nullable=True)
    created_by_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    email_id = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(200), nullable=True)
    is_private = db.Column(db.Boolean, default=False)

    addresses = db.relationship('Address', backref='contact', lazy=True)
    expenses = db.relationship(
        'Expenses', backref='contact', lazy=True)

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)


class AddressTypeLu(db.Model):
    """
    Hold's the address type lookup used while creating a new address.
    Can be edited by the master user
    """
    __tablename__ = "address_type_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    contacts = db.relationship('Address', backref='address_type', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'style_class': self.style_class
        }
        return json


class Address(db.Model):
    """
    Master table for Address.
    Used to store the address associated with the user contacts
    """
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    address_type_id = db.Column(db.Integer, db.ForeignKey(
        'address_type_lu.id'), nullable=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id'), nullable=False)
    created_by_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200), nullable=False)
    address_line3 = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    comments = db.Column(db.String(300), nullable=True)
    latitude = db.Column(db.String(100), nullable=True)
    longitude = db.Column(db.String(100), nullable=True)
    is_private = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)


class ExpenseTypeLu(db.Model):
    """ Master table for Expense Type
        Used to store the various expense types
    """
    __tablename__ = "expense_type_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    expenses = db.relationship('Expenses', backref='expense_type', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'style_class': self.style_class
        }
        return json


class ExpenseCategoryLu(db.Model):
    """ Master table for Expense Type
        Used to store the various expense types
    """
    __tablename__ = "expense_category_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    expenses = db.relationship(
        'Expenses', backref='expense_category', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'style_class': self.style_class
        }
        return json


class Expenses(db.Model):
    """ Master table for all expenses
        Used to store the expense incurred
    """
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    expense_type_id = db.Column(db.Integer, db.ForeignKey(
        'expense_type_lu.id'), nullable=True)
    expense_category_id = db.Column(db.Integer, db.ForeignKey(
        'expense_category_lu.id'), nullable=True)
    expenses_contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    expense_amount = db.Column(db.Numeric(10, 2), nullable=False)
    expense_date_time = db.Column(db.DateTime(), nullable=False,
                                  default=datetime.utcnow)
    description = db.Column(db.String(300), nullable=False)
    expense_details = db.relationship(
        'ExpenseDetails', backref='expense', lazy=True)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'type_id': self.expense_type_id,
            'type_name': self.expense_type.name,
            'category_id': self.expense_category_id,
            'category_name': self.expense_category.name,
            'expense_date': self.expense_date_time,
            'expense_amount': self.expense_amount,
            'description': self.description
        }
        return json


class UnitOfMeasurementLu(db.Model):
    """ Master table for all expense UOM
        Used to store expense uom lookups
    """
    __tablename__ = "unit_of_measurement_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    expense_details = db.relationship(
        'ExpenseDetails', backref='uom', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'style_class': self.style_class,
        }
        return json


class ExpenseDetails(db.Model):
    """ Master table for all expense items
        Used to store item level detail of an expense
    """
    __tablename__ = "expense_details"
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    expenses_id = db.Column(
        db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    uom_id = db.Column(db.Integer, db.ForeignKey(
        'unit_of_measurement_lu.id'), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    gross_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_on = db.Column(db.DateTime(), nullable=False)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.item_name,
            'uom_id': self.uom_id,
            'uom_name': self.uom.name,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'gross_price': self.gross_price,
            'created_on': self.created_on
        }
        return json
