"""Add ForeignKey to posts table

Revision ID: 0e24c1cbc6ac
Revises: 5fc4cda0b0f0
Create Date: 2023-11-01 09:11:33.494814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e24c1cbc6ac'
down_revision: Union[str, None] = '5fc4cda0b0f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fk", source_table="posts", referent_table="users",
        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
