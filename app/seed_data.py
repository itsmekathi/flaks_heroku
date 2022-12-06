from datetime import date, datetime
from .models import User, Role, Post, ToDoList, TaskStatusLu, TaskPriorityLu, TaskUrgencyLu, ToDoItem, \
    ToDoItemComments, AddressTypeLu, Address, ContactTypeLu, Contact, UnitOfMeasurementLu, ExpenseTypeLu, ExpenseCategoryLu,  Expenses, ExpenseDetails


def seed_initial_data(db):
    db.drop_all()
    db.create_all()

    # region User
    admin_user = User(active=True, username='admin', email='admin@123.com',
                      password='$2b$12$cNAuUAhCVvo3xVj/YoMzYOZ/4oUiqjWDvs81wnSxHX.hh0Yyo2oPK', image_file='default.jpg', first_name='admin', last_name='user')
    test_user = User(active=True, username='testuser', email='testuser@123.com',
                     password='$2b$12$cNAuUAhCVvo3xVj/YoMzYOZ/4oUiqjWDvs81wnSxHX.hh0Yyo2oPK', image_file='default.jpg', first_name='test', last_name='user')
    db.session.add(admin_user)
    db.session.commit()

    role_admin = Role(name='Admin')
    role_testuser = Role(name='TestUser')
    role_customer = Role(name='Customer')
    role_super_customer = Role(name='SuperCustomer')

    db.session.add(role_admin)
    db.session.add(role_testuser)
    db.session.add(role_customer)
    db.session.add(role_super_customer)
    db.session.commit()

    admin_user.roles = [role_admin, role_testuser,
                        role_customer, role_super_customer]
    test_user.roles = [role_testuser, role_customer]
    db.session.add(admin_user)
    db.session.add(test_user)
    db.session.commit()
    # endregion

    # region Lookup tables
    contact_type_friends = ContactTypeLu(
        name="Friends", description="All contacts who are my friends", icon="icon-contact-friends", style_class="style-contact-friends")
    contact_type_office = ContactTypeLu(
        name="Office", description="All contacts who have worked with me", icon="icon-contact-office", style_class="style-contact-office")
    contact_type_family = ContactTypeLu(
        name="Family", description="All contacts who are my family", icon="icon-contact-family", style_class="style-contact-family")
    contact_type_neighbours = ContactTypeLu(
        name="Neighbours", description="All contacts who are my neighbours", icon="icon-contact-neighbours", style_class="style-contact-neighbours")
    contact_type_shops = ContactTypeLu(
        name="Shops", description="All shops", icon="icon-contact-shops", style_class="style-contact-shops")
    db.session.add(contact_type_friends)
    db.session.add(contact_type_office)
    db.session.add(contact_type_family)
    db.session.add(contact_type_neighbours)
    db.session.add(contact_type_shops)
    db.session.commit()

    address_type_home = AddressTypeLu(
        name="Home", description="All addressess which is a house", icon="icon-home", style_class="style-home")
    address_type_business = AddressTypeLu(
        name="business", description="All addressess which are businesses ", icon="icon-business", style_class="style-business")
    address_type_billing = AddressTypeLu(
        name="Family", description="All billing addressess", icon="icon-billing", style_class="style-billing")
    address_type_shipping = AddressTypeLu(
        name="Neighbours", description="All shipping addresses", icon="icon-shipping", style_class="style-shipping")
    db.session.add(address_type_home)
    db.session.add(address_type_business)
    db.session.add(address_type_billing)
    db.session.add(address_type_shipping)
    db.session.commit()

    uom_type_kg = UnitOfMeasurementLu(
        name="Kilogram", description="All measurements in kilogram", icon="icon-kg", style_class="style-kg")
    uom_type_liters = UnitOfMeasurementLu(
        name="Liters", description="All measurements which are in liters", icon="icon-liters", style_class="style-liters")
    uom_type_eaches = UnitOfMeasurementLu(
        name="Eaches", description="All measurements which are in counts", icon="icon-eaches", style_class="style-eaches")
    uom_type_meter = UnitOfMeasurementLu(
        name="Meter", description="All measurements which are in meters", icon="icon-meter", style_class="style-meter")
    db.session.add(uom_type_kg)
    db.session.add(uom_type_liters)
    db.session.add(uom_type_eaches)
    db.session.add(uom_type_meter)
    db.session.commit()

    expense_type_fixed = ExpenseTypeLu(name="Fixed", description="All expenses which are fixed",
                                       icon="icon-expenses-fixed", style_class="style-expenses-fixed")
    expense_type_variable = ExpenseTypeLu(name="Variable", description="All expenses which are variable",
                                          icon="icon-expenses-variable", style_class="style-expenses-variable")
    expense_type_periodic = ExpenseTypeLu(name="Periodic", description="All expenses which are periodic eg: powerbill, rent",
                                          icon="icon-expenses-periodic", style_class="style-expenses-periodic")
    db.session.add(expense_type_fixed)
    db.session.add(expense_type_variable)
    db.session.add(expense_type_periodic)
    db.session.commit()

    expense_category_groceries = ExpenseCategoryLu(name="Grocery", description="All expenses which are for groceries",
                                                   icon="icon-expenses-category-grocery", style_class="style-expenses-category-grocery")
    expense_category_vegetables = ExpenseCategoryLu(name="Vegetables", description="All expenses which are for vegetables",
                                                    icon="icon-expenses-category-vegetables", style_class="style-expenses-category-vegetables")
    expense_category_utility = ExpenseCategoryLu(name="Utility", description="All expenses which are for utility like power, rent, maintainance",
                                                 icon="icon-expenses-category-utility", style_class="style-expenses-category-utility")
    expense_category_travel = ExpenseCategoryLu(name="Travel/Transport", description="All expenses which are for Travel or transport",
                                                icon="icon-expenses-category-travel", style_class="style-expenses-category-travel")
    db.session.add(expense_category_groceries)
    db.session.add(expense_category_vegetables)
    db.session.add(expense_category_utility)
    db.session.add(expense_category_travel)
    db.session.commit()

    status_created = TaskStatusLu(
        name='Created', description='A newly created task', style_class='green')
    status_approved = TaskStatusLu(
        name='Approved', description='An approved task', style_class='orange')
    status_assigned = TaskStatusLu(
        name='Assigned', description='An assigned task', style_class='green')
    status_inprogress = TaskStatusLu(
        name='InProgress', description='A task for which work has started', style_class='green')
    status_done = TaskStatusLu(
        name='Done', description='A task which has been completed', style_class='blue')

    db.session.add(status_created)
    db.session.add(status_approved)
    db.session.add(status_assigned)
    db.session.add(status_inprogress)
    db.session.add(status_done)

    db.session.commit()

    priority_p4 = TaskPriorityLu(
        name='P4', description='A low priority task', style_class='blue')
    priority_p3 = TaskPriorityLu(
        name='P3', description='A Medium priority task', style_class='green')
    priority_p2 = TaskPriorityLu(
        name='P2', description='A Priority task', style_class='orange')
    priority_p1 = TaskPriorityLu(
        name='P1', description='A High priority task', style_class='red')

    db.session.add(priority_p4)
    db.session.add(priority_p3)
    db.session.add(priority_p2)
    db.session.add(priority_p1)

    db.session.commit()

    urgency_u4 = TaskUrgencyLu(
        name='U4', description='A low urgency task', style_class='blue')
    urgency_u3 = TaskUrgencyLu(
        name='U3', description='A Medium urgency task', style_class='green')
    urgency_u2 = TaskUrgencyLu(
        name='U2', description='An Urgent task', style_class='orange')
    urgency_u1 = TaskUrgencyLu(
        name='U1', description='A high urgency task', style_class='red')

    db.session.add(urgency_u4)
    db.session.add(urgency_u3)
    db.session.add(urgency_u2)
    db.session.add(urgency_u1)

    db.session.commit()

    # endregion

    # region Posts
    admin_post1 = Post(title='Post-1', content='Content for Post-1',
                       author=admin_user, date_posted=datetime(2019, 10, 10))
    admin_post2 = Post(title='Post-2', content='Content for Post-2',
                       author=admin_user, date_posted=datetime(2019, 10, 11))
    admin_post3 = Post(title='Post-3', content='Content for Post-3',
                       author=admin_user, date_posted=datetime(2019, 10, 12))
    admin_post4 = Post(title='Post-4', content='Content for Post-4',
                       author=admin_user, date_posted=datetime(2019, 10, 13))
    admin_post5 = Post(title='Post-5', content='Content for Post-5',
                       author=admin_user, date_posted=datetime(2019, 10, 14))
    admin_post6 = Post(title='Post-6', content='Content for Post-6',
                       author=admin_user, date_posted=datetime(2019, 10, 15))
    admin_post7 = Post(title='Post-7', content='Content for Post-7',
                       author=admin_user, date_posted=datetime(2019, 10, 16))
    admin_post8 = Post(title='Post-8', content='Content for Post-8',
                       author=admin_user, date_posted=datetime(2019, 10, 17))

    testuser_post1 = Post(title='Post-1', content='Content for Post-1',
                          author=test_user, date_posted=datetime(2019, 10, 18))
    testuser_post2 = Post(title='Post-2', content='Content for Post-2',
                          author=test_user, date_posted=datetime(2019, 10, 19))
    testuser_post3 = Post(title='Post-3', content='Content for Post-3',
                          author=test_user, date_posted=datetime(2019, 10, 20))

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

    # endregion

    # region TodoLists
    admin_todo_list1 = ToDoList(title='Home-Improvements', description='All Home-improvements tasks',
                                user=admin_user, date_created=date(2019, 10, 10))
    admin_todo_list2 = ToDoList(title='Personal', description='All Personal tasks',
                                user=admin_user, date_created=date(2019, 10, 11))

    testuser_todo_list1 = ToDoList(
        title='Testing', description='All testing tasks', user=test_user, date_created=date(2019, 10, 10))

    db.session.add(admin_todo_list1)
    db.session.add(admin_todo_list2)
    db.session.add(testuser_todo_list1)

    db.session.commit()

    admin_todolist1_todoitem1 = ToDoItem(title='Paint windows', description='paint all the windows', todolist=admin_todo_list1, task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4, scheduled_date=datetime(2019, 11, 1),
                                         estimated_duration_hours=3, estimated_duration_minutes=30, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    admin_todolist1_todoitem2 = ToDoItem(title='Fix leaking', description='Fix all leaking by applying cement', todolist=admin_todo_list1, task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3, scheduled_date=datetime(2019, 11, 2),
                                         estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    admin_todolist1_todoitem3 = ToDoItem(title='Install tubelights', description='Install the new tube light', todolist=admin_todo_list1, task_status=status_assigned, task_priority=priority_p2, task_urgency=urgency_u2, scheduled_date=datetime(2019, 11, 5),
                                         estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))

    admin_todolist2_todoitem1 = ToDoItem(title='Learn Python', description='Learn python by following book Head first', todolist=admin_todo_list2, task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4, scheduled_date=datetime(2019, 11, 20),
                                         estimated_duration_hours=3, estimated_duration_minutes=30, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    admin_todolist2_todoitem2 = ToDoItem(title='Learn Flask', description='Learn Flask by following Miguels book', todolist=admin_todo_list2, task_status=status_inprogress, task_priority=priority_p2, task_urgency=urgency_u2, scheduled_date=datetime(2019, 11, 2),
                                         estimated_duration_hours=30, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    admin_todolist2_todoitem3 = ToDoItem(title='Learn Angular js', description='Learn angularJS integration with Flask', todolist=admin_todo_list2, task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3, scheduled_date=datetime(2019, 11, 10),
                                         estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))

    db.session.add(admin_todolist1_todoitem1)
    db.session.add(admin_todolist1_todoitem2)
    db.session.add(admin_todolist1_todoitem3)
    db.session.add(admin_todolist2_todoitem1)
    db.session.add(admin_todolist2_todoitem2)
    db.session.add(admin_todolist2_todoitem3)
    db.session.commit()

    admin_todolist1_todoitem1_comment1 = ToDoItemComments(
        comment="Created the task", todoitem=admin_todolist1_todoitem1, user=admin_user, comment_date=datetime(2019, 10, 10))
    admin_todolist1_todoitem1_comment2 = ToDoItemComments(
        comment="Started the task", todoitem=admin_todolist1_todoitem1, user=admin_user, comment_date=datetime(2019, 10, 11))
    admin_todolist1_todoitem1_comment3 = ToDoItemComments(
        comment="Finished the task", todoitem=admin_todolist1_todoitem1, user=admin_user, comment_date=datetime(2019, 10, 12))
    admin_todolist1_todoitem2_comment1 = ToDoItemComments(
        comment="Created the task", todoitem=admin_todolist1_todoitem2, user=admin_user, comment_date=datetime(2019, 10, 10))
    admin_todolist1_todoitem2_comment2 = ToDoItemComments(
        comment="Started the task", todoitem=admin_todolist1_todoitem2, user=admin_user, comment_date=datetime(2019, 10, 11))

    db.session.add(admin_todolist1_todoitem1_comment1)
    db.session.add(admin_todolist1_todoitem1_comment2)
    db.session.add(admin_todolist1_todoitem1_comment3)
    db.session.add(admin_todolist1_todoitem2_comment1)
    db.session.add(admin_todolist1_todoitem2_comment2)

    db.session.commit()

    testuser_todolist1_todoitem1 = ToDoItem(title='User creation', description='Test the User creation', todolist=testuser_todo_list1, task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4, scheduled_date=datetime(2019, 11, 1),
                                            estimated_duration_hours=3, estimated_duration_minutes=30, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    testuser_todolist1_todoitem2 = ToDoItem(title='Todo list-creation', description='Test new todo list creation', todolist=testuser_todo_list1, task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3, scheduled_date=datetime(2019, 11, 2),
                                            estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    testuser_todolist1_todoitem3 = ToDoItem(title='Test Todo items', description='Test creating, modification and deleting of todo items', todolist=testuser_todo_list1, task_status=status_assigned, task_priority=priority_p2, task_urgency=urgency_u2, scheduled_date=datetime(2019, 11, 5),
                                            estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    testuser_todolist1_todoitem4 = ToDoItem(title='Test statuses', description='Test creation, modification and deletion of statusus', todolist=testuser_todo_list1, task_status=status_created, task_priority=priority_p4, task_urgency=urgency_u4, scheduled_date=datetime(2019, 11, 20),
                                            estimated_duration_hours=3, estimated_duration_minutes=30, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    testuser_todolist1_todoitem5 = ToDoItem(title='Test priorities', description='Test creation, modification and deletion of priorities', todolist=testuser_todo_list1, task_status=status_inprogress, task_priority=priority_p2, task_urgency=urgency_u2, scheduled_date=datetime(2019, 11, 2),
                                            estimated_duration_hours=30, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))
    testuser_todolist1_todoitem6 = ToDoItem(title='Test urgencies', description='Test creation, modification and deletion of urgencies', todolist=testuser_todo_list1, task_status=status_approved, task_priority=priority_p3, task_urgency=urgency_u3, scheduled_date=datetime(2019, 11, 10),
                                            estimated_duration_hours=4, estimated_duration_minutes=45, date_created=datetime(2019, 11, 1), date_modified=datetime(2019, 11, 1))

    db.session.add(testuser_todolist1_todoitem1)
    db.session.add(testuser_todolist1_todoitem2)
    db.session.add(testuser_todolist1_todoitem3)
    db.session.add(testuser_todolist1_todoitem4)
    db.session.add(testuser_todolist1_todoitem5)
    db.session.add(testuser_todolist1_todoitem6)

    db.session.commit()
    # endregion

    # region Contacts
    local_store = Contact(contact_type=contact_type_shops, created_by=admin_user, first_name="Local",
                          last_name="Shop", email_id="local.shop@gmail.com", phone_number="12312312")
    amazon_store = Contact(contact_type=contact_type_shops, created_by=admin_user, first_name="Amazon",
                           last_name="India", email_id="amazonindia@gmail.com", phone_number="9237492874")
    db.session.add(local_store)
    db.session.add(amazon_store)
    db.session.commit()
    # endregion

    # region Address
    local_store_address = Address(address_type=address_type_business, contact=local_store, created_by=admin_user, address_line1="Fathima stores", address_line2="Nelegedranahalli",
                                  address_line3="nagasandra Post", city="Bangalore", state="Karnataka", country="India", comments="For all groceries buy from this store")
    amazon_store_address = Address(address_type=address_type_business, contact=amazon_store, created_by=admin_user, address_line1="Amazon stores",
                                   address_line2="Silicon valley", address_line3="california", city="LA", state="America west", country="America", comments="Amazon store usa")
    db.session.add(local_store_address)
    db.session.add(amazon_store_address)
    db.session.commit()
    # endregion

    admin_expense_grocery = Expenses(
        title="Buy Grocery", expense_type=expense_type_variable, expense_category=expense_category_groceries, contact=local_store, created_by=admin_user, expense_amount=100.00, description="Brought groceries from local store")
    admin_expense_book = Expenses(
        title="Buy Book", expense_type=expense_type_variable, expense_category=expense_category_utility, contact=amazon_store, created_by=admin_user, expense_amount=300.00, description="Brought programming books online")
    admin_expense_travel = Expenses(
        title="Travel to office", expense_type=expense_type_variable, expense_category=expense_category_travel, contact=local_store, created_by=admin_user, expense_amount=500.00, description="Travel to office from home")
    db.session.add(admin_expense_grocery)
    db.session.add(admin_expense_book)
    db.session.add(admin_expense_travel)
    db.session.commit()

    admin_grocery_expense_tomoto = ExpenseDetails(
        item_name="Tomoto", expense=admin_expense_grocery, uom=uom_type_kg, unit_price=10.00, quantity=5, gross_price=50)
    admin_grocery_expense_onion = ExpenseDetails(
        item_name="Onion", expense=admin_expense_grocery, uom=uom_type_kg, unit_price=20.00, quantity=2.5, gross_price=50)
    admin_expense_book_book1 = ExpenseDetails(
        item_name="Let us c", expense=admin_expense_book, uom=uom_type_eaches, unit_price=250.00, quantity=1, gross_price=250)
    admin_expense_book_book2 = ExpenseDetails(
        item_name="Let us c++", expense=admin_expense_book, uom=uom_type_eaches, unit_price=250.00, quantity=1, gross_price=250)

    db.session.add(admin_grocery_expense_tomoto)
    db.session.add(admin_grocery_expense_onion)
    db.session.add(admin_expense_book_book1)
    db.session.add(admin_expense_book_book2)
    db.session.commit()
