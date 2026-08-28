"""initial_tasks_table

Revision ID: 20260827_tasks
Revises: 8bdce163d209
Create Date: 2026-08-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '20260827_tasks'
down_revision: Union[str, Sequence[str], None] = '8bdce163d209'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'tasks',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column('capture_id', sa.Uuid(), nullable=True),
        sa.Column('parent_task_id', sa.Uuid(), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('task_type', sa.Text(), nullable=False, server_default='task'),
        sa.Column('status', sa.Text(), nullable=False, server_default='proposed'),
        sa.Column('task_instructions', sa.Text(), nullable=True),
        sa.Column('definition_of_done', sa.Text(), nullable=True),
        sa.Column('session_estimate_minutes', sa.Integer(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tasks_capture_id'), 'tasks', ['capture_id'], unique=False)
    op.create_index(op.f('ix_tasks_parent_task_id'), 'tasks', ['parent_task_id'], unique=False)
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_parent_task_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_capture_id'), table_name='tasks')
    op.drop_table('tasks')