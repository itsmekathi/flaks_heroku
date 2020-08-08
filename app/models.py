import hashlib
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
    lists = db.relationship('ListHeader', backref="created_by", lazy=True)
    journals = db.relationship(
        'PersonalJournal', backref="author", lazy='dynamic')
    bookmarks_folder = db.relationship(
        'BookmarksFolder', backref="created_by", lazy=True)
    bookmarks_items = db.relationship(
        'BookmarksItems', backref="created_by", lazy=True)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=self.gravatar_hash(), size=size, default=default, rating=rating)

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

    def to_json(self):
        json = {
            'id': self.id,
            'contactTypeId': self.contact_type_id,
            'firstName': self.first_name,
            'middleName': self.middle_name,
            'lastName': self.last_name,
            'emailId': self.email_id,
            'phoneNumber': self.phone_number
        }
        return json


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

    def to_json(self):
        json = {
            'id': self.id,
            'addressTypeid': self.address_type_id,
            'contactId': self.contact_id,
            'createdBy': self.created_by.username,
            'state': self.state,
            'city': self.state,
            'country': self.country,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'address_line3': self.address_line3
        }
        return json


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
            'styleClass': self.style_class,
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
            'expenseId': self.expenses_id,
            'uomId': self.uom_id,
            'uomName': self.uom.name,
            'unitPrice': self.unit_price,
            'quantity': self.quantity,
            'grossPrice': self.gross_price,
            'createdOn': self.created_on,
            'modifiedOn': self.modified_on,
            'url': url_for('expenses.detail_item', expense_id=self.expenses_id, expense_item_id=self.id)
        }
        return json


# All tables related to lists

class ListTypeLu(db.Model):
    """ Master table for List type
        Used to store the various list types eg., bookmarks, reminders, etc.,
    """
    __tablename__ = "list_type_lu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    style_class = db.Column(
        db.String(100), nullable=False, default="text-danger")
    sort_order = db.Column(db.Integer, nullable=False)
    lists = db.relationship(
        'ListHeader', backref='list_type', lazy=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'styleClass': self.style_class,
            'sortOrder': self.sort_order,
            'resourceUrl': url_for('api.list_type', type_id=self.id)
        }
        return json


class ListHeader(db.Model):
    """ Master table for all list header.
        Should contain the title and sort orders
    """
    __tablename__ = "list_header"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey(
        'list_type_lu.id'), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    sort_order = db.Column(db.Integer, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    list_items = db.relationship('ListItem', backref="list_header", lazy=True)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'type': self.list_type.name,
            'description': self.description,
            'sortOrder': self.sort_order,
            'createdBy': self.created_by.username,
            'createdOn': self.created_on,
            'modifiedOn': self.modified_on,
            'resourceUrl': url_for('api.list_header', list_id=self.id,),
            'detailUrl': url_for('lists.list_details', list_id=self.id, ajax=1)
        }
        return json


class ListItem(db.Model):
    """ Master table for all list detail.
        Should contain the list detail
    """
    __tablename__ = "list_item"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'list_header.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    sort_order = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'stars': self.stars,
            'sortOrder': self.sort_order,
            'createdOn': self.created_on,
            'modifiedOn': self.modified_on,
            'updateUrl': url_for('api.list_item', list_id=self.list_id)
        }
        return json


class BookmarksFolder(db.Model):
    """
    Master table for all bookmark folder.
    Will contain all folders under which book marks are stored
    """
    __tablename__ = "bookmarks_folder"
    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    bookmark_items = db.relationship(
        'BookmarksItems', backref="bookmark_folder", lazy=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.folder_name,
            'description': self.description,
            'createdOn': self.created_on,
            'modifiedOn': self.modified_on,
        }
        return json


class BookmarksItems(db.Model):
    """
    ## Master table for all bookmark items.
    ### Will contain only bookmarks with parent folder_id which can be nullable
    """
    __tablename__ = "bookmark_items"
    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, db.ForeignKey(
        'bookmarks_folder.id'), nullable=True)
    resource_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(
        db.DateTime(), nullable=True)

    def to_json(self):
        json = {
            'id': self.id,
            'folder_id': self.folder_id,
            'url': self.resource_url,
            'description': self.description,
            'createdOn': self.created_on,
            'modifiedOn': self.modified_on,
        }
        return json


# Models for journal flow

class PersonalJournal(db.Model):
    __tablename__ = 'personal_journal'
    id = db.Column(db.Integer, primary_key=True)
    tag_line = db.Column(db.String(300))
    body_html = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    modified_on = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_private = db.Column(db.Boolean(),
                           nullable=False, server_default='1')
