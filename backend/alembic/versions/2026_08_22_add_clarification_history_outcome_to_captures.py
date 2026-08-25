"""add_clarification_history_to_captures

Revision ID: 8bdce163d209
Revises: 6c2b3e6c0287
Create Date: 2026-08-22 17:39:38.985624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8bdce163d209'
down_revision: Union[str, Sequence[str], None] = '6c2b3e6c0287'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('captures', sa.Column('clarification_history', sa.JSON(), nullable=False, server_default='[]'))
    op.add_column('captures', sa.Column('outcome', sa.Text(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('captures', 'outcome')
    op.drop_column('captures', 'clarification_history')
