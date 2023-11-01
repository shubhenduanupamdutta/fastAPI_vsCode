"""Create Post Table

Revision ID: edb028a4a09d
Revises:
Create Date: 2023-11-01 08:43:24.893970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edb028a4a09d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
