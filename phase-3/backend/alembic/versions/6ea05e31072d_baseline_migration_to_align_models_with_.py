"""Baseline migration to align models with database

Revision ID: 6ea05e31072d
Revises: 7967e81e7e0f
Create Date: 2026-01-08 23:07:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ea05e31072d'
down_revision: Union[str, None] = '7967e81e7e0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This is a baseline migration to align the migration history with the current database state.
    # The tables already exist and are properly configured, so no changes are needed.
    pass


def downgrade() -> None:
    # No changes to revert since this is a baseline alignment migration
    pass