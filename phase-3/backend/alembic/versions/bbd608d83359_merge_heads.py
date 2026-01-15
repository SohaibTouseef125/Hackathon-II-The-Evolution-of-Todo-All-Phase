"""merge heads

Revision ID: bbd608d83359
Revises: 20260114_add_tool_calls, 4751db3e15e6
Create Date: 2026-01-14 23:42:30.902051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbd608d83359'
down_revision: Union[str, None] = ('20260114_add_tool_calls', '4751db3e15e6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
