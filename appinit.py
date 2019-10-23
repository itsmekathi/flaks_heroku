def init_app():
    from app import create_app, db
    myapp = create_app('development')
    from app.models import User, Role, UserRoles, Post, ToDoList, ToDoItem
    myapp.app_context().push()
    db.drop_all()
    db.create_all()

    # populate dummy data
    
