"""Add tool_calls column to message table

Revision ID: 20260114_add_tool_calls
Revises:
Create Date: 2026-01-14 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime
from sqlmodel import Session, SQLModel, Field
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '20260114_add_tool_calls'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add the tool_calls column to the message table
    op.add_column('message', sa.Column('tool_calls', sa.String(), nullable=True))


def downgrade():
    # Drop the tool_calls column from the message table
    op.drop_column('message', 'tool_calls')