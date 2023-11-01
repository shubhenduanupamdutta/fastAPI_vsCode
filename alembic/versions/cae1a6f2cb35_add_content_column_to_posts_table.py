"""Add content column to posts table

Revision ID: cae1a6f2cb35
Revises: edb028a4a09d
Create Date: 2023-11-01 08:51:48.445596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cae1a6f2cb35'
down_revision: Union[str, None] = 'edb028a4a09d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
