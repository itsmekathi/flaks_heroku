import os
import sys
import click
from app import create_app, db
from app.models import User, Role, UserRoles, Post, ToDoList, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItem, ToDoItemComments
from flask_migrate import Migrate
from datetime import datetime, date


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, UserRoles=UserRoles, Post=Post, ToDoList=ToDoList, TaskStatusLu = TaskStatusLu,
     TaskPriorityLu = TaskPriorityLu, TaskUrgencyLu=TaskUrgencyLu , ToDoItem = ToDoItem, ToDoItemComments = ToDoItemComments )

# @app.cli.command()
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command("dropdb")
def drop_db():
    """Run this command to drop all the tables in db."""
    db.drop_all()

@app.cli.command("createdb")
def create_db():
    """Runs the command to create the tables in db."""
    db.create_all()

@app.cli.command()
def populateseeddata():
    """Run this command to populate dummy data into db."""
    admin_user = User(active=True, username='admin', email='admin@123.com', password='$2b$12$cNAuUAhCVvo3xVj/YoMzYOZ/4oUiqjWDvs81wnSxHX.hh0Yyo2oPK', image_file='default.jpg', first_name='admin', last_name='user')
    test_user = User(active=True, username='testuser', email='testuser@123.com', password='$2b$12$cNAuUAhCVvo3xVj/YoMzYOZ/4oUiqjWDvs81wnSxHX.hh0Yyo2oPK', image_file='default.jpg', first_name='test', last_name='user')
    db.session.add(admin_user)
    db.session.commit()

    # Populate the roles data
    role_admin = Role(name='Admin')
    role_testuser = Role(name='TestUser')
    role_customer = Role(name='Customer')
    role_super_customer = Role(name='SuperCustomer')

    db.session.add(role_admin)
    db.session.add(role_testuser)
    db.session.add(role_customer)
    db.session.add(role_super_customer)
    db.session.commit()

    admin_user.roles =[role_admin, role_testuser, role_customer, role_super_customer]
    test_user.roles =[role_testuser, role_customer]
    db.session.add(admin_user)
    db.session.add(test_user)
    db.session.commit()

    # Populate some posts for both users
    admin_post1 = Post(title='Post-1', content='Content for Post-1', author=admin_user, date_posted= datetime(2019,10,10))
    admin_post2 = Post(title='Post-2', content='Content for Post-2', author=admin_user, date_posted= datetime(2019,10,11))
    admin_post3 = Post(title='Post-3', content='Content for Post-3', author=admin_user, date_posted= datetime(2019,10,12))
    admin_post4 = Post(title='Post-4', content='Content for Post-4', author=admin_user, date_posted= datetime(2019,10,13))
    admin_post5 = Post(title='Post-5', content='Content for Post-5', author=admin_user, date_posted= datetime(2019,10,14))
    admin_post6 = Post(title='Post-6', content='Content for Post-6', author=admin_user, date_posted= datetime(2019,10,15))
    admin_post7 = Post(title='Post-7', content='Content for Post-7', author=admin_user, date_posted= datetime(2019,10,16))
    admin_post8 = Post(title='Post-8', content='Content for Post-8', author=admin_user, date_posted= datetime(2019,10,17))

    testuser_post1 = Post(title='Post-1', content='Content for Post-1', author=test_user, date_posted= datetime(2019,10,18))
    testuser_post2 = Post(title='Post-2', content='Content for Post-2', author=test_user, date_posted= datetime(2019,10,19))
    testuser_post3 = Post(title='Post-3', content='Content for Post-3', author=test_user, date_posted= datetime(2019,10,20))

    db.session.add(admin_post1)
    db.session.add(admin_post2)
    db.session.add(admin_post3)
    db.session.add(admin_post4)
    db.session.add(admin_post5)
    db.session.add(admin_post6)
    db.session.add(admin_post7)
    db.session.add(admin_post8)

    db.session.add(testuser_post1)
    db.session.add(testuser_post2)
    db.session.add(testuser_post3)

    db.session.commit()


    # Populate task_status
    status_created = TaskStatusLu(name='Created',description='A newly created task', style_class='green')
    status_approved = TaskStatusLu(name='Approved',description='An approved task', style_class='orange')
    status_assigned = TaskStatusLu(name='Assigned',description='An assigned task', style_class='green')
    status_inprogress = TaskStatusLu(name='InProgress',description='A task for which work has started', style_class='green')
    status_done = TaskStatusLu(name='Done',description='A task which has been completed', style_class='blue')

    db.session.add(status_created)
    db.session.add(status_approved)
    db.session.add(status_assigned)
    db.session.add(status_inprogress)
    db.session.add(status_done)

    db.session.commit()

    # Populate task_priority
    priority_p4 = TaskPriorityLu(name='P4', description='A low priority task', style_class='blue')
    priority_p3 = TaskPriorityLu(name='P3', description='A Medium priority task', style_class='green')
    priority_p2 = TaskPriorityLu(name='P2', description='A Priority task', style_class='orange')
    priority_p1 = TaskPriorityLu(name='P1', description='A High priority task', style_class='red')

    db.session.add(priority_p4)
    db.session.add(priority_p3)
    db.session.add(priority_p2)
    db.session.add(priority_p1)

    db.session.commit()

    # Populate task_urgency
    urgency_u4 = TaskUrgencyLu(name='U4', description='A low urgency task', style_class='blue')
    urgency_u3 = TaskUrgencyLu(name='U3', description='A Medium urgency task', style_class='green')
    urgency_u2 = TaskUrgencyLu(name='U2', description='An Urgent task', style_class='orange')
    urgency_u1 = TaskUrgencyLu(name='U1', description='A high urgency task', style_class='red')

    db.session.add(urgency_u4)
    db.session.add(urgency_u3)
    db.session.add(urgency_u2)
    db.session.add(urgency_u1)

    db.session.commit()

    # Populate new todo-list for both users
    admin_todo_list1 = ToDoList(title='Home-Improvements',description='All Home-improvements tasks', user=admin_user, date_created=date(2019,10,10))
    admin_todo_list2 = ToDoList(title='Personal',description='All Personal tasks', user=admin_user, date_created=date(2019,10,11))

    testuser_todo_list1 = ToDoList(title='Testing',description='All testing tasks', user=test_user, date_created=date(2019,10,10))

    db.session.add(admin_todo_list1)
    db.session.add(admin_todo_list2)
    db.session.add(testuser_todo_list1)

    db.session.commit()


    admin_todolist1_todoitem1 = ToDoItem(title='Paint windows', description='paint all the windows', todolist = admin_todo_list1 ,task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4,scheduled_date=datetime(2019,11,1),
    estimated_duration_hours=3, estimated_duration_minutes=30,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    admin_todolist1_todoitem2 = ToDoItem(title='Fix leaking', description='Fix all leaking by applying cement', todolist = admin_todo_list1 ,task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3,scheduled_date=datetime(2019,11,2),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    admin_todolist1_todoitem3 = ToDoItem(title='Install tubelights', description='Install the new tube light', todolist = admin_todo_list1 ,task_status=status_assigned, task_priority=priority_p2, task_urgency=urgency_u2,scheduled_date=datetime(2019,11,5),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))

    admin_todolist2_todoitem1 = ToDoItem(title='Learn Python', description='Learn python by following book Head first', todolist = admin_todo_list2 ,task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4,scheduled_date=datetime(2019,11,20),
    estimated_duration_hours=3, estimated_duration_minutes=30,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    admin_todolist2_todoitem2 = ToDoItem(title='Learn Flask', description='Learn Flask by following Miguels book', todolist = admin_todo_list2 ,task_status=status_inprogress, task_priority=priority_p2, task_urgency=urgency_u2,scheduled_date=datetime(2019,11,2),
    estimated_duration_hours=30, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    admin_todolist2_todoitem3 = ToDoItem(title='Learn Angular js', description='Learn angularJS integration with Flask', todolist = admin_todo_list2 ,task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3,scheduled_date=datetime(2019,11,10),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))

    db.session.add(admin_todolist1_todoitem1)
    db.session.add(admin_todolist1_todoitem2)
    db.session.add(admin_todolist1_todoitem3)
    db.session.add(admin_todolist2_todoitem1)
    db.session.add(admin_todolist2_todoitem2)
    db.session.add(admin_todolist2_todoitem3)
    db.session.commit()

    admin_todolist1_todoitem1_comment1 = ToDoItemComments(comment="Created the task",todoitem=admin_todolist1_todoitem1, user=admin_user,comment_date=datetime(2019,10,10))
    admin_todolist1_todoitem1_comment2 = ToDoItemComments(comment="Started the task",todoitem=admin_todolist1_todoitem1, user=admin_user,comment_date=datetime(2019,10,11))
    admin_todolist1_todoitem1_comment3 = ToDoItemComments(comment="Finished the task",todoitem=admin_todolist1_todoitem1, user=admin_user,comment_date=datetime(2019,10,12))
    admin_todolist1_todoitem2_comment1 = ToDoItemComments(comment="Created the task",todoitem=admin_todolist1_todoitem2, user=admin_user,comment_date=datetime(2019,10,10))
    admin_todolist1_todoitem2_comment2 = ToDoItemComments(comment="Started the task",todoitem=admin_todolist1_todoitem2, user=admin_user,comment_date=datetime(2019,10,11))

    db.session.add(admin_todolist1_todoitem1_comment1)
    db.session.add(admin_todolist1_todoitem1_comment2)
    db.session.add(admin_todolist1_todoitem1_comment3)
    db.session.add(admin_todolist1_todoitem2_comment1)
    db.session.add(admin_todolist1_todoitem2_comment2)

    db.session.commit()

    testuser_todolist1_todoitem1 = ToDoItem(title='User creation', description='Test the User creation', todolist = testuser_todo_list1 ,task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4,scheduled_date=datetime(2019,11,1),
    estimated_duration_hours=3, estimated_duration_minutes=30,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    testuser_todolist1_todoitem2 = ToDoItem(title='Todo list-creation', description='Test new todo list creation', todolist = testuser_todo_list1 ,task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3,scheduled_date=datetime(2019,11,2),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    testuser_todolist1_todoitem3 = ToDoItem(title='Test Todo items', description='Test creating, modification and deleting of todo items', todolist = testuser_todo_list1 ,task_status=status_assigned, task_priority=priority_p2, task_urgency=urgency_u2,scheduled_date=datetime(2019,11,5),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    testuser_todolist1_todoitem4 = ToDoItem(title='Test statuses', description='Test creation, modification and deletion of statusus', todolist = testuser_todo_list1 ,task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4,scheduled_date=datetime(2019,11,20),
    estimated_duration_hours=3, estimated_duration_minutes=30,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    testuser_todolist1_todoitem5 = ToDoItem(title='Test priorities', description='Test creation, modification and deletion of priorities', todolist = testuser_todo_list1 ,task_status=status_inprogress, task_priority=priority_p2, task_urgency=urgency_u2,scheduled_date=datetime(2019,11,2),
    estimated_duration_hours=30, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))
    testuser_todolist1_todoitem6 = ToDoItem(title='Test urgencies', description='Test creation, modification and deletion of urgencies', todolist = testuser_todo_list1 ,task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3,scheduled_date=datetime(2019,11,10),
    estimated_duration_hours=4, estimated_duration_minutes=45,date_created=datetime(2019,11,1), date_modified=datetime(2019,11,1))

    db.session.add(testuser_todolist1_todoitem1)
    db.session.add(testuser_todolist1_todoitem2)
    db.session.add(testuser_todolist1_todoitem3)
    db.session.add(testuser_todolist1_todoitem4)
    db.session.add(testuser_todolist1_todoitem5)
    db.session.add(testuser_todolist1_todoitem6)

    db.session.commit()


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test(coverage):
    """ Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html'%covdir)
        COV.erase()
