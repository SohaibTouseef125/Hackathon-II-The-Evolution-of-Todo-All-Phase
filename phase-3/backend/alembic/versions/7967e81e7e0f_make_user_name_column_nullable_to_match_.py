"""Make user name column nullable to match model

Revision ID: 7967e81e7e0f
Revises: a1e89635d81f
Create Date: 2026-01-08 23:01:00.321588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7967e81e7e0f'
down_revision: Union[str, None] = 'a1e89635d81f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make the name column nullable to match the model
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=True)


def downgrade() -> None:
    # Make the name column not nullable, but first update any null values to empty string
    op.execute("UPDATE \"user\" SET name = '' WHERE name IS NULL")
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=False)