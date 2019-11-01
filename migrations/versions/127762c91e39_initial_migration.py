"""initial migration

Revision ID: 127762c91e39
Revises: 
Create Date: 2019-11-01 22:13:50.592422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127762c91e39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('task_priority_lu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('style_class', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('task_status_lu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('style_class', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('task_urgency_lu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('style_class', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=255, collation='NOCASE'), nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('first_name', sa.String(length=100, collation='NOCASE'), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=100, collation='NOCASE'), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('priority_id', sa.Integer(), nullable=False),
    sa.Column('urgency_id', sa.Integer(), nullable=False),
    sa.Column('todo_list_id', sa.Integer(), nullable=False),
    sa.Column('scheduled_date', sa.DateTime(), nullable=False),
    sa.Column('estimated_duration_hours', sa.Integer(), nullable=False),
    sa.Column('estimated_duration_minutes', sa.Integer(), nullable=False),
    sa.Column('actual_duration_hours', sa.Integer(), nullable=False),
    sa.Column('actual_duration_minutes', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['priority_id'], ['task_priority_lu.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['task_status_lu.id'], ),
    sa.ForeignKeyConstraint(['todo_list_id'], ['todo_lists.id'], ),
    sa.ForeignKeyConstraint(['urgency_id'], ['task_urgency_lu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_item_worklogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('todo_item_id', sa.Integer(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('comment', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['todo_item_id'], ['todo_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_items_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=300), nullable=False),
    sa.Column('todo_item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['todo_item_id'], ['todo_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_items_comments')
    op.drop_table('todo_item_worklogs')
    op.drop_table('todo_items')
    op.drop_table('user_roles')
    op.drop_table('todo_lists')
    op.drop_table('post')
    op.drop_table('users')
    op.drop_table('task_urgency_lu')
    op.drop_table('task_status_lu')
    op.drop_table('task_priority_lu')
    op.drop_table('roles')
    # ### end Alembic commands ###
