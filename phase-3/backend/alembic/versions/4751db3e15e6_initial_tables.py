"""initial tables

Revision ID: 4751db3e15e6
Revises: a78bfa006670
Create Date: 2026-01-09 01:19:46.551618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4751db3e15e6'
down_revision: Union[str, None] = 'a78bfa006670'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This is a placeholder migration.
    # No changes needed.
    pass


def downgrade() -> None:
    # No changes to revert since this is a placeholder migration
    pass