import os
import sys
import click
import pytz
from app import create_app, db
from app.models import User, Role, UserRoles, Post, ToDoList, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItem, \
    ToDoItemComments

from flask_migrate import Migrate, upgrade
from app.seed_data import seed_initial_data
from flask import session

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, UserRoles=UserRoles, Post=Post, ToDoList=ToDoList, TaskStatusLu=TaskStatusLu,
                TaskPriorityLu=TaskPriorityLu, TaskUrgencyLu=TaskUrgencyLu, ToDoItem=ToDoItem, ToDoItemComments=ToDoItemComments)


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
    """Run this command to populate dummy data into db.
    Will drop and create all tables."""
    seed_initial_data(db=db)


# Unit testing and code coverage
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
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest version
    upgrade()

    # create or update data

# Custom currency filter for indian currency
@app.template_filter()
def conv_curr_inr(amount):
    """Custom currency filter for indian rupee"""
    from babel.numbers import format_currency
    return format_currency(amount, 'INR', locale='en_IN')


@app.template_filter('localtime')
def localtime_filter(value):
    '''Use timezone from the session object, if available, to localize datetimes from UTC.'''
    if 'timezone' not in session:
        return value

    # https://stackoverflow.com/a/34832184
    utc_dt = pytz.utc.localize(value)
    local_tz = pytz.timezone(session['timezone'])
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt