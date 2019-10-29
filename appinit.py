from app.models import User, Role, UserRoles, Post, ToDoList, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItem, ToDoItemComments
from app import create_app, db
myapp = create_app('development')
myapp.app_context().push()
db.drop_all()
db.create_all()

# Populate initial data

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



