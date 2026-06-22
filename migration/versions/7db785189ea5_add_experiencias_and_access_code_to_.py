"""add experiencias and access_code to coaches

Revision ID: 7db785189ea5
Revises: 05e9978a4a36
Create Date: 2026-06-15 10:19:13.262358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7db785189ea5'
down_revision: Union[str, Sequence[str], None] = '05e9978a4a36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass