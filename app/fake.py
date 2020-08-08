from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, PersonalJournal


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 image_file='default.jpg',
                 password='password',
                 first_name=fake.name(),
                 last_name=fake.name())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def journals(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        j = PersonalJournal(body_html=fake.text(), tag_line='tag_line' + str(i), is_private=False,
                            author=u)
        db.session.add(j)
    db.session.commit()
