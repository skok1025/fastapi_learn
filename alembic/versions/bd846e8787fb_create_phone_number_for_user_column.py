"""Create phone number for user column

Revision ID: bd846e8787fb
Revises: 
Create Date: 2024-08-26 13:50:42.800880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd846e8787fb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
