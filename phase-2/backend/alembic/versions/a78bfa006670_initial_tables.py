"""initial tables

Revision ID: a78bfa006670
Revises: 6ea05e31072d
Create Date: 2026-01-09 00:26:49.649098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a78bfa006670'
down_revision: Union[str, None] = '6ea05e31072d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This migration was created incorrectly, tables already exist.
    # No changes needed.
    pass


def downgrade() -> None:
    # No changes to revert since this is a placeholder migration
    pass